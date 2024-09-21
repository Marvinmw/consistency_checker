// SPDX-License-Identifier: GPL-3.0

pragma solidity 0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BlueHorizonToken is Ownable, ERC20 {
    uint256 public constant MONTH_IN_SECONDS = 30 * 86400;
    uint256 public constant MAX_SUPPLY = 100000000e18; // 100,000,000

    uint256 public constant SEED_SALE = 3500000e18; // 3.5%
    uint256 public constant PRIVATE_SALE = 15500000e18; // 15.5%
    uint256 public constant PUBLIC_SALE = 3000000e18; // 3%
    uint256 public constant LIQUIDITY = 5000000e18; // 5%

    uint256 public constant TEAM = 8000000e18; // 8%
    uint256 public constant ADVISOR = 5000000e18; // 5%
    uint256 public constant DEVELOPMENT = 10000000e18; // 10%
    uint256 public constant MARKETING = 10000000e18; // 10%
    uint256 public constant FARMING = 40000000e18; // 40%

    uint256 public initTime;

    address public masterChef;
    address public nftMasterChef;

    uint256 public seedSaleUnlocked = 0;
    uint256 public privateSaleUnlocked = 0;
    uint256 public teamUnlocked = 0;
    uint256 public advisorUnlocked = 0;
    uint256 public developmentUnlocked = 0;
    uint256 public marketingUnlocked = 0;
    uint256 public farmingUnlocked = 0;

    constructor(uint256 _initTime, address _recipient) ERC20("BlueHorizon", "BLH") {
        initTime = _initTime != 0 ? _initTime : block.timestamp;

        uint256 totalUnlocked = 0;
        totalUnlocked += PUBLIC_SALE;
        totalUnlocked += LIQUIDITY;
        _mint(_recipient, totalUnlocked);
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual override {
        super._beforeTokenTransfer(from, to, amount);

        if (from == address(0)) {
            require(
                totalSupply() + amount <= MAX_SUPPLY,
                "BlueHorizonToken::_beforeTokenTransfer::MAX_SUPPLY_EXCEEDED"
            );
        }
    }

    /**
     * @dev mint tokens for masterChef
     * callable by masterChef contracts only
     */
    function mint(address _recipient, uint256 _amount) public {
        require(msg.sender == masterChef || msg.sender == nftMasterChef, "BlueHorizonToken::mint::MASTER_ONLY");
        require(FARMING >= _amount, "BlueHorizonToken::mint::LIMIT_EXCEEDED");

        uint256 amount = mintableFarming();
        amount = amount > _amount ? _amount : amount;
        if (amount > 0) {
            farmingUnlocked += amount;
            _mint(_recipient, amount);
        }
    }

    /**
     * @dev mintable tokens for farming
     */
    function mintableFarming() public view returns (uint256) {
        if (initTime == 0) return 0;
        uint256 startReleasing = initTime;
        if (startReleasing > block.timestamp) return 0;

        uint256 gap = block.timestamp - startReleasing;
        uint256 months = gap / MONTH_IN_SECONDS + 1;
        uint256 totalMintable = (months * FARMING) / 24;
        if (totalMintable > FARMING) {
            totalMintable = FARMING;
        }
        return totalMintable - farmingUnlocked;
    }

    /**
     * @dev mintable tokens for seed sale
     */
    function mintableSeedSale() public view returns (uint256) {
        if (initTime == 0) return 0;
        uint256 startReleasing = initTime;
        if (startReleasing > block.timestamp) return 0;

        uint256 gap = block.timestamp - startReleasing;
        uint256 months = gap / MONTH_IN_SECONDS + 1;
        uint256 totalMintable = (months * SEED_SALE) / 12;
        if (totalMintable > SEED_SALE) {
            totalMintable = SEED_SALE;
        }
        return totalMintable - seedSaleUnlocked;
    }

    /**
     * @dev mintable tokens for private sale
     */
    function mintablePrivateSale() public view returns (uint256) {
        if (initTime == 0) return 0;
        uint256 startReleasing = initTime;
        if (startReleasing > block.timestamp) return 0;

        uint256 gap = block.timestamp - startReleasing;
        uint256 months = gap / MONTH_IN_SECONDS + 1;
        uint256 totalMintable = (months * PRIVATE_SALE) / 6;
        if (totalMintable > PRIVATE_SALE) {
            totalMintable = PRIVATE_SALE;
        }
        return totalMintable - privateSaleUnlocked;
    }

    /**
     * @dev mintable tokens for team
     */
    function mintableTeam() public view returns (uint256) {
        if (initTime == 0) return 0;
        uint256 startReleasing = initTime + 3 * MONTH_IN_SECONDS;
        if (startReleasing > block.timestamp) return 0;

        uint256 gap = block.timestamp - startReleasing;
        uint256 months = gap / MONTH_IN_SECONDS + 1;
        uint256 totalMintable = (months * TEAM) / 15;
        if (totalMintable > TEAM) {
            totalMintable = TEAM;
        }
        return totalMintable - teamUnlocked;
    }

    /**
     * @dev mintable tokens for advisor
     */
    function mintableAdvisor() public view returns (uint256) {
        if (initTime == 0) return 0;
        uint256 startReleasing = initTime + 3 * MONTH_IN_SECONDS;
        if (startReleasing > block.timestamp) return 0;

        uint256 gap = block.timestamp - startReleasing;
        uint256 months = gap / MONTH_IN_SECONDS + 1;
        uint256 totalMintable = (months * ADVISOR) / 9;
        if (totalMintable > ADVISOR) {
            totalMintable = ADVISOR;
        }
        return totalMintable - advisorUnlocked;
    }

    /**
     * @dev mintable tokens for development
     */
    function mintableDevelopment() public view returns (uint256) {
        if (initTime == 0) return 0;
        uint256 startReleasing = initTime + 1 * MONTH_IN_SECONDS;
        if (startReleasing > block.timestamp) return 0;

        uint256 gap = block.timestamp - startReleasing;
        uint256 months = gap / MONTH_IN_SECONDS + 1;
        uint256 totalMintable = (months * DEVELOPMENT) / 23;
        if (totalMintable > DEVELOPMENT) {
            totalMintable = DEVELOPMENT;
        }
        return totalMintable - developmentUnlocked;
    }

    /**
     * @dev mintable tokens for marketing
     */
    function mintableMarketing() public view returns (uint256) {
        if (initTime == 0) return 0;
        uint256 startReleasing = initTime + 1 * MONTH_IN_SECONDS;
        if (startReleasing > block.timestamp) return 0;

        uint256 gap = block.timestamp - startReleasing;
        uint256 months = gap / MONTH_IN_SECONDS + 1;
        uint256 totalMintable = (months * MARKETING) / 23;
        if (totalMintable > MARKETING) {
            totalMintable = MARKETING;
        }
        return totalMintable - marketingUnlocked;
    }

    /**
     * @dev mint tokens for seed sale
     * callable by owner
     */
    function mintSeedSale(address _recipient) external onlyOwner {
        uint256 mintable = mintableSeedSale();
        if (mintable > 0) {
            seedSaleUnlocked += mintable;
            _mint(_recipient, mintable);
        }
    }

    /**
     * @dev mint tokens for private sale
     * callable by owner
     */
    function mintPrivateSale(address _recipient) external onlyOwner {
        uint256 mintable = mintablePrivateSale();
        if (mintable > 0) {
            privateSaleUnlocked += mintable;
            _mint(_recipient, mintable);
        }
    }

    /**
     * @dev mint tokens for team
     * callable by owner
     */
    function mintTeam(address _recipient) external onlyOwner {
        uint256 mintable = mintableTeam();
        if (mintable > 0) {
            teamUnlocked += mintable;
            _mint(_recipient, mintable);
        }
    }

    /**
     * @dev mint tokens for advisor
     * callable by owner
     */
    function mintAdvisor(address _recipient) external onlyOwner {
        uint256 mintable = mintableAdvisor();
        if (mintable > 0) {
            advisorUnlocked += mintable;
            _mint(_recipient, mintable);
        }
    }

    /**
     * @dev mint tokens for development
     * callable by owner
     */
    function mintDevelopment(address _recipient) external onlyOwner {
        uint256 mintable = mintableDevelopment();
        if (mintable > 0) {
            developmentUnlocked += mintable;
            _mint(_recipient, mintable);
        }
    }

    /**
     * @dev mint tokens for marketing
     * callable by owner
     */
    function mintMarketing(address _recipient) external onlyOwner {
        uint256 mintable = mintableMarketing();
        if (mintable > 0) {
            marketingUnlocked += mintable;
            _mint(_recipient, mintable);
        }
    }

    /**
     * @dev set masterChef
     * callable by owner
     */
    function setMaster(address _masterChef) external onlyOwner {
        require(_masterChef != address(0), "BlueHorizonToken::setMaster::INVALID");
        masterChef = _masterChef;
    }

    /**
     * @dev set nftMasterChef
     * callable by owner
     */
    function setNftMaster(address _masterChef) external onlyOwner {
        require(_masterChef != address(0), "BlueHorizonToken::setNftMaster::INVALID");
        nftMasterChef = _masterChef;
    }
}
