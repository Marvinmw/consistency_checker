pragma solidity ^0.5.8;


contract TokenWrapper {
    using SafeMath for uint;
    using SafeERC20 for IERC20;

    IERC20 public tokenAddr = IERC20(0x7C86085332482654D31De8576eFDEf0E25284b9e); // BEST
    
    uint private _totalSupply;
    
    struct Info {
        uint balance;
        uint unstakeTime;
        uint freeValue; // free value for each period
        uint withdrawedValue;
    }
    
    uint public FreezeTime = 3 minutes;
    uint public UnfreezePercent = 12; // 1/12
    
    mapping(address => Info) private _balances;

    function totalSupply() public view returns (uint) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint) {
        return _balances[account].balance;
    }
    
    function withdrawableInfo(address account) public view returns (uint withdrawableValue, uint nextPeriod, uint nextPeriodWithdrawableValue) {
        if (0 == _balances[account].balance) {
            return (0, 0, 0);
        }
        
        uint startTime =  _balances[account].unstakeTime;
        uint period = now.sub(startTime).div(FreezeTime);
        
        nextPeriod = period.add(1).mul(FreezeTime).add(startTime);
        if (nextPeriod > startTime.add(12 * FreezeTime)) {
            nextPeriod = startTime.add(12 * FreezeTime);
        }
        withdrawableValue = _balances[account].freeValue.mul(period).sub(_balances[account].withdrawedValue);
        nextPeriodWithdrawableValue = withdrawableValue.add(_balances[account].freeValue);
        if (withdrawableValue > _balances[account].balance) {
            withdrawableValue = _balances[account].balance;
        }
        if (nextPeriodWithdrawableValue > _balances[account].balance) {
            nextPeriodWithdrawableValue = _balances[account].balance;
        }
        
        return (withdrawableValue, nextPeriod, nextPeriodWithdrawableValue);
    }

    function stake(uint amount) internal {
        tokenAddr.safeTransferFrom(msg.sender, address(this), amount);
         
        _totalSupply = _totalSupply.add(amount);
        
        _balances[msg.sender].unstakeTime = now;
        _balances[msg.sender].withdrawedValue = 0;
        
        _balances[msg.sender].balance = _balances[msg.sender].balance.add(amount);
        _balances[msg.sender].freeValue = _balances[msg.sender].balance.div(UnfreezePercent);
    }

    function withdraw(uint amount) public {
        (uint withdrawable,,) = withdrawableInfo(msg.sender);
        require(amount <= withdrawable, "invalid withdraw amount");
        
        _totalSupply = _totalSupply.sub(amount);
        _balances[msg.sender].balance = _balances[msg.sender].balance.sub(amount);
        _balances[msg.sender].withdrawedValue = _balances[msg.sender].withdrawedValue.add(amount);
        tokenAddr.safeTransfer(msg.sender, amount);
    }
}

// library Objects {
//     struct User {
//         address addr;
//         uint uid;
//         uint pid;
//         uint childCnt;
//         uint [2]reward; // 0: btc, 1: eth; 2: musk
//     }
// }

contract BEST_MINE_Pool is TokenWrapper, Ownable {
    using Address for address;
    using SafeMath for uint;

    event Staked(address indexed user, uint amount);
    event Withdrawn(address indexed user, uint amount);

    constructor () public {
        newUser(msg.sender, 0);
    }

    mapping(address => uint) public addr2uid_;
    mapping(uint => Objects.User) public uid2User_;
    uint userCnt_;

    IERC20 public BTCToken = IERC20(0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c);
    IERC20 public ETHToken = IERC20(0x2170Ed0880ac9A755fd29B2688956BD959F933F8);
    uint btcReward;
    uint ethReward;
    
    struct Reward {
        address addr;
        uint btc;
        uint eth;
        uint withdrawBtc;
        uint withdrawEth;
    }
    
    mapping(uint => Reward) public rewardMap;
    
    function max_uid() public view returns (uint) {
        return userCnt_;
    }

    function getUID(address addr) public view returns (uint) {
        return addr2uid_[addr];
    }

    function newUser0(address addr, uint pid) internal returns (uint) {
        uint uid = addr2uid_[addr];
        if (uid > 0) {
            return uid;
        }

        userCnt_ = userCnt_ + 1;
        uid = userCnt_;
        
        if (pid == uid) {
            pid = 1;
        }
        if (pid >= userCnt_) {
            pid = 1;
        }
        if (uid == 1) {
            pid = 0;
        } else if (pid == 0) {
            pid = 1;
        }
        uid2User_[pid].childCnt = uid2User_[pid].childCnt + 1;
        uid2User_[uid].addr = addr;
        uid2User_[uid].uid = uid;
        uid2User_[uid].pid = pid;
        addr2uid_[addr] = uid;
        return uid;
    }

    function getParent(address addr) public view returns (address) {
        uint uid = addr2uid_[addr];
        return (
            uid2User_[uid2User_[uid].pid].addr
        );
    }
    
    function getGrandparent(address addr) public view returns (address) {
        uint uid = addr2uid_[addr];
        return (
            uid2User_[uid2User_[uid2User_[uid].pid].pid].addr
        );
    }

    function incParentReward(address addr, uint idx, uint amount) internal returns (bool) {
        uint uid = addr2uid_[addr];
        
        if (uid > 0 && uid2User_[uid].pid > 0 && idx < uid2User_[uid].reward.length) {
            uid = uid2User_[uid].pid;
            uid2User_[uid].reward[idx] = uid2User_[uid].reward[idx].add(amount);
            return true;
        }
        return false;
    }

    function getInviteInfo(address addr) public view returns (address parent, uint childCnt, uint [2]memory) {
        uint uid = addr2uid_[addr];
        return (getParent(addr), uid2User_[uid].childCnt, uid2User_[uid].reward);
    }
    
    function newUser(address addr, uint inviterID) internal {
        uint uid = addr2uid_[addr];
    
        if (uid == 0) {
            uid = newUser0(addr, inviterID);
            rewardMap[uid].addr = addr;
        }
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
    
    function incBtcPoolBalance(uint amount) public returns (bool) {
        BTCToken.safeTransferFrom(msg.sender, address(this), amount);
        btcReward = btcReward.add(amount);

        return true;
    }
    
    function incEthPoolBalance(uint amount) public returns (bool) {
        ETHToken.safeTransferFrom(msg.sender, address(this), amount);
        ethReward = ethReward.add(amount);

        return true;
    }

    function resetRewardBalance() public onlyOwner returns (bool) {
        btcReward = 0;
        ethReward = 0;

        return true;
    }

    function getRewardBalance() public view returns (uint, uint) {
        return (btcReward, ethReward);
    }
    
    function setReward(address []memory user, uint []memory btc, uint [] memory eth) public onlyOwner returns (uint) {
        require(user.length > 0 && user.length == btc.length && user.length == eth.length, "invalid input");
        uint idx = 0;
        uint uid = 0;
        for (; idx < user.length; idx++) {
            uid = addr2uid_[user[idx]];
            if (uid > 0) {
                rewardMap[uid].btc = rewardMap[uid].btc.add(btc[idx]);
                rewardMap[uid].eth = rewardMap[uid].eth.add(eth[idx]);
            }
        }
        return idx;
    }
    
    function getStakeInfo(uint s, uint cnt) public view returns (address[] memory addrList, uint[] memory uidList, uint [] memory stakeAmountList) {
        uint idx = s;
        uint maxUID = max_uid();
        if (idx > maxUID) {
            return (new address[](0), new uint[](0), new uint[](0));
        }
        if (idx + cnt > maxUID) {
            cnt = maxUID - idx + 1;
        }
        addrList = new address[](cnt);
        uidList = new uint[](cnt);
        stakeAmountList = new uint[](cnt);
        
        for (; idx < s + cnt; idx++) {
            addrList[idx-s] = rewardMap[idx].addr;
            uidList[idx-s] = addr2uid_[rewardMap[idx].addr];
            stakeAmountList[idx-s] = balanceOf(rewardMap[idx].addr);
        }
        
        return (addrList, uidList, stakeAmountList);
    }
    
    function reward(address user) public view returns (uint btc, uint eth, uint witdrawBtc, uint withdrawEth) {
        uint uid = addr2uid_[user];
        return (
            rewardMap[uid].btc,
            rewardMap[uid].eth,
            rewardMap[uid].withdrawBtc,
            rewardMap[uid].withdrawEth
        );
    }
    
    uint inviteRewardRate = 10;
    function setInviteRewardRate(uint val) public onlyOwner returns (bool) {
        require(val < 100, "invalid invite rate");
        inviteRewardRate = val;
        return true;
    }
    
    function getReward() public returns (bool) {
        uint val = 0;
        uint uid = addr2uid_[msg.sender];
        address parent = getParent(msg.sender);
        if (rewardMap[uid].btc > 0 && BTCToken.balanceOf(address(this)) >= rewardMap[uid].btc) {
            val = rewardMap[uid].btc;
            rewardMap[uid].btc = 0;
            rewardMap[uid].withdrawBtc = rewardMap[uid].withdrawBtc.add(val);
            BTCToken.transfer(msg.sender, val);
            
            val = val.mul(inviteRewardRate).div(100);
            if (BTCToken.balanceOf(address(this)) >= val && address(0) != parent) {
                BTCToken.transfer(parent, val);
                incParentReward(msg.sender, 0, val);
            }
        }
        if (rewardMap[uid].eth > 0 && ETHToken.balanceOf(address(this)) >= rewardMap[uid].eth) {
            val = rewardMap[uid].eth;
            rewardMap[uid].eth = 0;
            rewardMap[uid].withdrawEth = rewardMap[uid].withdrawEth.add(val);
            ETHToken.transfer(msg.sender, val);
            
            val = val.mul(inviteRewardRate).div(100);
            if (ETHToken.balanceOf(address(this)) >= val && address(0) != parent) {
                ETHToken.transfer(parent, val);
                incParentReward(msg.sender, 1, val);
            }
        }
        return true;
    }
    
    function setFreezeTime(uint val) public onlyOwner returns (uint) {
        uint oldVal = FreezeTime;
        FreezeTime = val;
        return oldVal;
    }

    function setStakeToken(address token) public onlyOwner returns (bool) {
        tokenAddr = IERC20(token);
        return true;
    }

    function setBTC(address token) public onlyOwner returns (bool) {
        BTCToken = IERC20(token);
        return true;
    }

    function setETH(address token) public onlyOwner returns (bool) {
        ETHToken = IERC20(token);
        return true;
    }
    
    function BTCBalance() public view returns (uint) {
        return BTCToken.balanceOf(address(this));
    }
    
    function ETHBalance() public view returns (uint) {
        return ETHToken.balanceOf(address(this));
    }

    function stake(uint amount, uint inviterID) public checkLock {
        require(amount > 0, "Cannot stake 0");
        newUser(msg.sender, inviterID);
        super.stake(amount);
        emit Staked(msg.sender, amount);
    }

    function withdraw(uint amount) public {
        require(amount > 0, "Cannot withdraw 0");
        super.withdraw(amount);
        emit Withdrawn(msg.sender, amount);
    }

    function rescue(address payable to_, uint amount_) external onlyOwner {
        require(to_ != address(0), "must not 0");
        require(amount_ > 0, "must gt 0");

        to_.transfer(amount_);
    }

    function rescue(address to_, address token_, uint amount_) external onlyOwner {
        require(to_ != address(0), "must not 0");
        require(amount_ > 0, "must gt 0");

        require(token_ != address(BTCToken), "invalid token");
        require(token_ != address(ETHToken), "invalid token");
        require(token_ != address(tokenAddr), "invalid token");

        IERC20(token_).transfer(to_, amount_);
    }
}
