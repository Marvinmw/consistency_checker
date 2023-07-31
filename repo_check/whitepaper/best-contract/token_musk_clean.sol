pragma solidity ^0.5.8;



contract Token_MUSK is ERC20Detailed, ERC20 {
    using Address for address;
    using SafeMath for uint;

    uint public decimalVal;

    constructor () public ERC20Detailed("MUSK", "MUSK", 6) {
        decimalVal = 10 ** 6;
        _mint(msg.sender, 10000000*decimalVal);
    }
    
    function mint(address to, uint amount) public onlyOwner returns (bool) {
        require(address(0) != to, "invalid address");
        require(amount > 0, "invalid amount");
        
        _mint(to, amount);
        
        return true;
    }

    function rescue(address payable to_, uint256 amount_) external onlyOwner {
        require(to_ != address(0), "must not 0");
        require(amount_ > 0, "must gt 0");

        to_.transfer(amount_);
    }

    function rescue(address to_, address token_, uint256 amount_) external onlyOwner {
        require(to_ != address(0), "must not 0");
        require(amount_ > 0, "must gt 0");

        IERC20(token_).transfer(to_, amount_);
    }
}
