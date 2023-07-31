pragma solidity ^0.5.8;

library Address {

    function isContract(address account) internal view returns (bool) {
        bytes32 codehash;
        bytes32 accountHash = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
        assembly { codehash := extcodehash(account) }
        return (codehash != 0x0 && codehash != accountHash);
    }

    function toPayable(address account) internal pure returns (address payable) {
        return address(uint160(account));
    }

    function sendValue(address payable recipient, uint amount) internal {
        require(address(this).balance >= amount, "Address: insufficient balance");

        (bool success, ) = recipient.call.value(amount)("");
        require(success, "Address: unable to send value, recipient may have reverted");
    }
}

contract Context {
    constructor () internal { }

    function _msgSender() internal view returns (address payable) {
        return msg.sender;
    }

    function _msgData() internal view returns (bytes memory) {
        this;
        return msg.data;
    }
}

interface IERC20 {
    function totalSupply() external view returns (uint);
    function balanceOf(address account) external view returns (uint);
    function transfer(address recipient, uint amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint);
    function approve(address spender, uint amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint amount) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
}

library Math {
    function max(uint a, uint b) internal pure returns (uint) {
        return a >= b ? a : b;
    }

    function min(uint a, uint b) internal pure returns (uint) {
        return a < b ? a : b;
    }

    function average(uint a, uint b) internal pure returns (uint) {
        return (a / 2) + (b / 2) + ((a % 2 + b % 2) / 2);
    }
}

contract Ownable is Context {
    address private _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor () internal {
        _owner = _msgSender();
        emit OwnershipTransferred(address(0), _owner);
    }

    function owner() public view returns (address) {
        return _owner;
    }

    modifier onlyOwner() {
        require(isOwner(), "Ownable: caller is not the owner");
        _;
    }

    function isOwner() public view returns (bool) {
        return _msgSender() == _owner;
    }

    function renounceOwnership() public onlyOwner {
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }

    function transferOwnership(address newOwner) public onlyOwner {
        _transferOwnership(newOwner);
    }

    function _transferOwnership(address newOwner) internal {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }
}

library SafeMath {

    function add(uint a, uint b) internal pure returns (uint) {
        uint c = a + b;
        require(c >= a, "SafeMath: addition overflow");

        return c;
    }

    function sub(uint a, uint b) internal pure returns (uint) {
        return sub(a, b, "SafeMath: subtraction overflow");
    }

    function sub(uint a, uint b, string memory errorMessage) internal pure returns (uint) {
        require(b <= a, errorMessage);
        uint c = a - b;

        return c;
    }

    function mul(uint a, uint b) internal pure returns (uint) {

        if (a == 0) {
            return 0;
        }

        uint c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");

        return c;
    }

    function div(uint a, uint b) internal pure returns (uint) {
        return div(a, b, "SafeMath: division by zero");
    }

    function div(uint a, uint b, string memory errorMessage) internal pure returns (uint) {
        require(b > 0, errorMessage);
        uint c = a / b;

        return c;
    }

    function mod(uint a, uint b) internal pure returns (uint) {
        return mod(a, b, "SafeMath: modulo by zero");
    }

    function mod(uint a, uint b, string memory errorMessage) internal pure returns (uint) {
        require(b != 0, errorMessage);
        return a % b;
    }
}

library SafeERC20 {
    using SafeMath for uint;
    using Address for address;

    function safeTransfer(IERC20 token, address to, uint value) internal {
        callOptionalReturn(token, abi.encodeWithSelector(token.transfer.selector, to, value));
    }

    function safeTransferFrom(IERC20 token, address from, address to, uint value) internal {
        callOptionalReturn(token, abi.encodeWithSelector(token.transferFrom.selector, from, to, value));
    }

    function safeApprove(IERC20 token, address spender, uint value) internal {

        require((value == 0) || (token.allowance(address(this), spender) == 0),
            "SafeERC20: approve from non-zero to non-zero allowance"
        );
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, value));
    }

    function safeIncreaseAllowance(IERC20 token, address spender, uint value) internal {
        uint newAllowance = token.allowance(address(this), spender).add(value);
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, newAllowance));
    }

    function safeDecreaseAllowance(IERC20 token, address spender, uint value) internal {
        uint newAllowance = token.allowance(address(this), spender).sub(value, "SafeERC20: decreased allowance below zero");
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, newAllowance));
    }

    function callOptionalReturn(IERC20 token, bytes memory data) private {

        require(address(token).isContract(), "SafeERC20: call to non-contract");

        (bool success, bytes memory returndata) = address(token).call(data);
        require(success, "SafeERC20: low-level call failed");

        if (returndata.length > 0) { // Return data is optional
            require(abi.decode(returndata, (bool)), "SafeERC20: TRC20 operation did not succeed");
        }
    }
}

contract TokenWrapper {
    using SafeMath for uint;
    using SafeERC20 for IERC20;

    IERC20 public tokenAddr = IERC20(0x77b447D0F17cdd135f56fA84180917B16F7ab2B1); // USDT
    
    uint private _totalSupply;
    
    struct Info {
        uint balance;
    }
    
    mapping(address => Info) private _balances;

    function totalSupply() public view returns (uint) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint) {
        return _balances[account].balance;
    }
    
    function stake(uint amount) public {
        tokenAddr.safeTransferFrom(msg.sender, address(this), amount);
        _totalSupply = _totalSupply.add(amount);
        _balances[msg.sender].balance = _balances[msg.sender].balance.add(amount);
    }

    function withdraw(uint amount) public {
        _totalSupply = _totalSupply.sub(amount);
        _balances[msg.sender].balance = _balances[msg.sender].balance.sub(amount);
        tokenAddr.safeTransfer(msg.sender, amount);
    }
}

contract Mine_MUSK_USDT_LP_Pool is TokenWrapper, Ownable {
    IERC20 public rewardToken = IERC20(0x13fB5Df6E37430248BFADd5a4EFf52A5a7B160b9); // MASK
    uint public constant DURATION = 365 days;

    uint public starttime = 1614556800; // 2021-03-01 00:00:00
    uint public periodFinish = 0;
    uint public rewardPerDuration = 0;
    uint public rewardDuration;
    uint public lastUpdateTime;
    uint public rewardPerTokenStored;
    uint public rewardRateAdjustTime = 0;

    mapping(address => uint) public userRewardPerTokenPaid;
    mapping(address => uint) public rewards;

    event Staked(address indexed user, uint amount);
    event Withdrawn(address indexed user, uint amount);
    
    address public communityAddr;
    uint communityRate = 15;

    constructor() public{
        starttime = now;
        periodFinish = starttime.add(DURATION);
        rewardPerDuration = uint(7500) * 1e6;
        rewardDuration = 1 days;
        rewardRateAdjustTime = starttime;
        communityAddr = msg.sender;
    }
    
    uint periodDuration = 30 days;
    
    function setCommunityAddr(address addr) public onlyOwner {
        communityAddr = addr;
    }

    bool public lock;
    function setLock(bool flag) public onlyOwner returns (bool) {
        lock = flag;
        return true;
    }
    
    modifier checkLock {
        require(lock == false, "locked");
        _;
    }

    
    function setPeriodDuration(uint duration) public onlyOwner returns (bool) {
        require(periodDuration > 0, "invalid period duration");
        periodDuration = duration;
        
        return true;
    }

    function adjustRewardRate() internal {
        if (rewardRateAdjustTime.sub(starttime).div(periodDuration) >= 12) {
            return;
        }
        if (now >= rewardRateAdjustTime + periodDuration) {
            uint changeRate = now.sub(rewardRateAdjustTime).div(periodDuration);
            rewardRateAdjustTime = rewardRateAdjustTime + changeRate.mul(periodDuration);
            rewardPerDuration = rewardPerDuration * (85 ** changeRate) / (100 ** changeRate);
        }
    }

    function setStakeToken(address token) public onlyOwner returns (bool) {
        tokenAddr = IERC20(token);
        return true;
    }

    function setRewardToken(address token) public onlyOwner returns (bool) {
        rewardToken = IERC20(token);
        return true;
    }

    function setStartTime(uint val) public onlyOwner returns (bool) {
        if (val == 0) {
            val = now;
        }
        starttime = val;
        lastUpdateTime = val;
        periodFinish = starttime.add(DURATION);
        adjustRewardRate();
        return true;
    }

    modifier updateReward(address account) {
        adjustRewardRate();
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = lastTimeRewardApplicable();
        if (account != address(0)) {
            rewards[account] = earned(account);
            userRewardPerTokenPaid[account] = rewardPerTokenStored;
        }
        _;
    }

    function lastTimeRewardApplicable() public view returns (uint) {
        return Math.min(block.timestamp, periodFinish);
    }

    function rewardPerToken() public view returns (uint) {
        if (totalSupply() == 0) {
            return rewardPerTokenStored;
        }
        return
        rewardPerTokenStored.add(
            lastTimeRewardApplicable()
            .sub(lastUpdateTime)
            .mul(rewardPerDuration).div(rewardDuration)
            .mul(1e18)
            .div(totalSupply())
        );
    }

    function earned(address account) public view returns (uint) {
        return
        balanceOf(account)
        .mul(rewardPerToken().sub(userRewardPerTokenPaid[account]))
        .div(1e18)
        .add(rewards[account]);
    }

    function stake(uint amount) public checkLock updateReward(msg.sender) {
        require(amount > 0, "Cannot stake 0");
        super.stake(amount);
        emit Staked(msg.sender, amount);
    }

    function withdraw(uint amount) public checkLock updateReward(msg.sender) {
        require(amount > 0, "Cannot withdraw 0");
        super.withdraw(amount);
        emit Withdrawn(msg.sender, amount);
    }

    function withdrawAndGetReward(uint amount) public updateReward(msg.sender) {
        require(amount <= balanceOf(msg.sender), "Cannot withdraw exceed the balance");
        withdraw(amount);
        getReward();
    }

    function exit() external {
        withdraw(balanceOf(msg.sender));
        getReward();
    }

    function getReward() public updateReward(msg.sender) checkLock {
        uint trueReward = earned(msg.sender);
        if (trueReward > 0) {
            rewards[msg.sender] = 0;
            uint rate = 100;
            rewardToken.safeTransfer(msg.sender, trueReward.mul(rate).div(100));
            rewardToken.safeTransfer(communityAddr, trueReward.mul(communityRate).div(100));
        }
    }

    function modifyReward(uint reward) external onlyOwner updateReward(address(0))
    {
        rewardPerDuration = reward;
    }
    
    function modifyRewardDuration(uint duration) public onlyOwner updateReward(address(0)) {
        require(duration > 0, "invalid duration");
        rewardDuration = duration;
    }
    
    function rescue(address payable to_, uint amount_) external onlyOwner {
        require(to_ != address(0), "must not 0");
        require(amount_ > 0, "must gt 0");

        to_.transfer(amount_);
    }

    function rescue(address to_, address token_, uint amount_) external onlyOwner {
        require(to_ != address(0), "must not 0");
        require(amount_ > 0, "must gt 0");

        require(token_ != address(rewardToken), "invalid token");
        require(token_ != address(tokenAddr), "invalid token");

        IERC20(token_).transfer(to_, amount_);
    }
}