// SPDX-License-Identifier: MIT LICENSE

//Dracore Version

pragma solidity 0.8.4;
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Etern is ERC20, Ownable {
  using SafeMath for uint256;

  mapping(address => uint256) private _balances;
  mapping(address => bool) controllers;

  uint256 private _totalSupply;
  uint256 private MAXSUP;
  uint256 constant MAXIMUMSUPPLY=100000000*10**18;

  constructor() ERC20("Etern", "ETRN") { 
      _mint(msg.sender, 1 * 10 ** 18);

  }

  function mint(address to, uint256 amount) external {
    require(controllers[msg.sender], "Only controllers can mint");
    require((MAXSUP+amount)<=MAXIMUMSUPPLY,"Maximum supply has been reached");
    _totalSupply = _totalSupply.add(amount);
    MAXSUP=MAXSUP.add(amount);
    _balances[to] = _balances[to].add(amount);
    _mint(to, amount);
  }

  
  function addController(address controller) external onlyOwner {
    controllers[controller] = true;
  }

  function removeController(address controller) external onlyOwner {
    controllers[controller] = false;
  }
  
  function totalSupply() public override view returns (uint256) {
    return _totalSupply;
  }

  function maxSupply() public  pure returns (uint256) {
    return MAXIMUMSUPPLY;
  }

}
