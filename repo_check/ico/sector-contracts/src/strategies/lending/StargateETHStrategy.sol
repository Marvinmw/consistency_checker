// SPDX-License-Identifier: MIT
pragma solidity 0.8.16;

import { IERC20, SafeERC20 } from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import { SafeETH } from "../../libraries/SafeETH.sol";
import { HarvestSwapParams } from "../../interfaces/Structs.sol";
import { IStargateRouter, lzTxObj } from "../../interfaces/stargate/IStargateRouter.sol";
import { IStargatePool } from "../../interfaces/stargate/IStargatePool.sol";
import { StarChefFarm, FarmConfig } from "../../strategies/adapters/StarChefFarm.sol";
import { StratAuthLight } from "../../common/StratAuthLight.sol";
import { ISCYStrategy } from "../../interfaces/ERC5115/ISCYStrategy.sol";
import { IWETH } from "../../interfaces/uniswap/IWETH.sol";

// import "hardhat/console.sol";

/// @title StargateETHStrategy
/// @notice this contract is a modified version of StargateStrategy
/// the changes are needed because Stargate ETH pools use a custom stgETH wrapper / instead of WETH
/// this wrapper automatically unwraps ETH on transfer
/// because SCYVaults interact with strategies using WETH and not native ETH, the current strategy
/// needs to unrap ETH and wrap it into stgETH before depositing into the pool
/// and wrap ETH into WETH after redeeming from the pool (calling instantRedeemLocal)
contract StargateETHStrategy is StarChefFarm, StratAuthLight, ISCYStrategy {
	using SafeERC20 for IERC20;

	IStargatePool public stargatePool;
	IStargateRouter public stargateRouter;
	IERC20 public underlying;
	IWETH public stargateETH;
	uint16 pId;

	constructor(
		address _vault,
		address _stargatePool,
		address _stargateRouter,
		uint16 _pId,
		address _underlying,
		address _stargateETH,
		FarmConfig memory _farmConfig
	) StarChefFarm(_farmConfig) {
		vault = _vault;
		pId = _pId;
		stargateETH = IWETH(_stargateETH);
		stargatePool = IStargatePool(_stargatePool);
		stargateRouter = IStargateRouter(_stargateRouter);
		underlying = IERC20(_underlying);
		IERC20(address(stargateETH)).safeIncreaseAllowance(_stargateRouter, type(uint256).max);
		IERC20(stargatePool).safeIncreaseAllowance(address(farm), type(uint256).max);
	}

	receive() external payable {}

	function deposit(uint256 amount) public onlyVault returns (uint256) {
		// need to unwrap from WETH and wrap into stgETH first
		IWETH(address(underlying)).withdraw(amount);
		stargateETH.deposit{ value: amount }();
		stargateRouter.addLiquidity(pId, amount, address(this));
		uint256 lp = stargatePool.balanceOf(address(this));
		_depositIntoFarm(lp);
		return lp;
	}

	function redeem(address recipient, uint256 amount)
		public
		onlyVault
		returns (uint256 amountOut)
	{
		if (amount == 0) return 0;
		_withdrawFromFarm(amount);

		// this is ugly but we have to do this to support the expected SCYVault flow
		// because SCYVault expects the strategy to send WETH, not ETH
		amountOut = stargateRouter.instantRedeemLocal(pId, amount, address(this));
		IWETH(address(underlying)).deposit{ value: amountOut }();
		underlying.safeTransfer(recipient, amountOut);
	}

	function harvest(HarvestSwapParams[] calldata params, HarvestSwapParams[] calldata)
		external
		onlyVault
		returns (uint256[] memory harvested, uint256[] memory)
	{
		uint256 amountOut = _harvestFarm(params[0]);
		if (amountOut > 0) deposit(amountOut);
		harvested = new uint256[](1);
		harvested[0] = amountOut;
		return (harvested, new uint256[](0));
	}

	function getAndUpdateTvl() external override returns (uint256) {
		return getTvl();
	}

	function getTvl() public view returns (uint256) {
		(uint256 balance, ) = farm.userInfo(uint256(farmId), address(this));
		return IStargatePool(stargatePool).amountLPtoLD(balance);
	}

	function closePosition(uint256) public onlyVault returns (uint256) {
		(uint256 balance, ) = farm.userInfo(farmId, address(this));
		_withdrawFromFarm(balance);
		uint256 amountOut = stargateRouter.instantRedeemLocal(pId, balance, address(this));
		IWETH(address(underlying)).deposit{ value: amountOut }();
		underlying.safeTransfer(address(vault), amountOut);
		return amountOut;
	}

	function getMaxTvl() external view returns (uint256) {
		return stargatePool.totalLiquidity() / 5; // 20% of total deposits
	}

	function collateralToUnderlying() external view returns (uint256) {
		return IStargatePool(stargatePool).amountLPtoLD(1e18);
	}

	function getLpToken() public view returns (address) {
		return address(stargatePool);
	}

	function getLpBalance() public view returns (uint256) {
		return _getFarmLp();
	}

	function getWithdrawAmnt(uint256 lpTokens) public view returns (uint256) {
		return IStargatePool(stargatePool).amountLPtoLD(lpTokens);
	}

	function getDepositAmnt(uint256 uAmnt) public view returns (uint256) {
		return ((uAmnt * 1e18) / IStargatePool(stargatePool).amountLPtoLD(1e18));
	}

	// EMERGENCY GUARDIAN METHODS
	function redeemRemote(
		uint16 _dstChainId,
		uint256 _srcPoolId,
		uint256 _dstPoolId,
		address payable _refundAddress,
		uint256 _amountLP,
		uint256 _minAmountLD,
		bytes calldata _to,
		lzTxObj memory _lzTxParams
	) external payable onlyVault {
		stargateRouter.redeemRemote(
			_dstChainId,
			_srcPoolId,
			_dstPoolId,
			_refundAddress,
			_amountLP,
			_minAmountLD,
			_to,
			_lzTxParams
		);
	}

	function redeemLocal(
		uint16 _dstChainId,
		uint256 _srcPoolId,
		uint256 _dstPoolId,
		address payable _refundAddress,
		uint256 _amountLP,
		bytes calldata _to,
		lzTxObj memory _lzTxParams
	) external payable onlyVault {
		stargateRouter.redeemLocal(
			_dstChainId,
			_srcPoolId,
			_dstPoolId,
			_refundAddress,
			_amountLP,
			_to,
			_lzTxParams
		);
	}

	function sendCredits(
		uint16 _dstChainId,
		uint256 _srcPoolId,
		uint256 _dstPoolId,
		address payable _refundAddress
	) external payable onlyVault {
		stargateRouter.sendCredits(_dstChainId, _srcPoolId, _dstPoolId, _refundAddress);
	}
}
