// SPDX-License-Identifier: MIT LICENSE

//Dracore Version

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

pragma solidity ^0.8.4;

contract EternumlandNft is ERC721Enumerable, Ownable {

    
    using Strings for uint256;
    string public baseURI;
    string public baseExtension = ".json";
    uint256 public maxSupply = 6000;
    uint256 public maxMintAmount = 50;
    bool public paused = false;
    uint8 public friendP = 10;
    uint8 public address1P = 2;
    uint8 public address2P = 2;
    uint8 public address3P = 2;
    uint8 public address4P = 2;
    uint8 public liquidityP = 15;
    uint8 public marketAdvSecurityP = 31;
    uint8 public developmentP = 8;
    uint8 public legalP = 18;
    uint256 private mintPermit;
    uint256 public cost = 800000000000000000;
    uint256 public Fcost = 720000000000000000;
    address private address1;
    address private address2;
    address private address3;
    address private address4;
    address private liquidity;
    address private marketAdvSecurity;
    address private development;
    address private legal;

    constructor() ERC721("Eternumland NFT", "ETRNLD") {}

    function _baseURI() internal view virtual override returns (string memory) {
    return "ipfs://QmPk1boUFfzhAoEzTfrp7iLs2Zk1Lo53aSMEeGnpDSu3gB/";

    }
    
    function mint(address _to, uint256 _mintAmount, address _code, uint256 _mintPermit) public payable {
           
            uint256 supply = totalSupply();
            require (!paused);
            require (_mintAmount > 0);
            require (_mintAmount <= maxMintAmount);
            require (supply + _mintAmount <= maxSupply);
            require (_code != _to);
            require (_mintPermit == mintPermit);

            // Treasury NFT
            payable(_code).transfer(msg.value / 100 * friendP);
            payable(address1).transfer(msg.value / 100 * address1P);
            payable(address2).transfer(msg.value / 100 * address2P);
            payable(address3).transfer(msg.value / 100 * address3P);
            payable(address4).transfer(msg.value / 100 * address4P);
            payable(liquidity).transfer(msg.value /100 * liquidityP);
            payable(marketAdvSecurity).transfer(msg.value /100 * marketAdvSecurityP);
            payable(development).transfer(msg.value /100 * developmentP);
            payable(legal).transfer(msg.value /100 * legalP);

               if (msg.sender != owner()) {
                    if (supply <= 500) {
                        require(msg.value >= cost/2 * _mintAmount || msg.value>= Fcost/2 * _mintAmount);
                    } else {
                    require(msg.value >= cost * _mintAmount || msg.value>= Fcost * _mintAmount);
                } 
                } 

            for (uint256 i = 1; i <= _mintAmount; i++) {
                _safeMint(_to, supply + i);
            
        
            }
    }


       function walletOfOwner(address _owner)
        public
        view
        returns (uint256[] memory)
        {
            uint256 ownerTokenCount = balanceOf(_owner);
            uint256[] memory tokenIds = new uint256[](ownerTokenCount);
            for (uint256 i; i < ownerTokenCount; i++) {
                tokenIds[i] = tokenOfOwnerByIndex(_owner, i);
            }
            return tokenIds;
        }
    
        
        function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory) {
            require(
                _exists(tokenId),
                "ERC721Metadata: URI query for nonexistent token"
                );
                
                string memory currentBaseURI = _baseURI();
                return
                bytes(currentBaseURI).length > 0 
                ? string(abi.encodePacked(currentBaseURI, tokenId.toString(), baseExtension))
                : "";
        }
        // only owner
        
        function setmaxMintAmount(uint256 _newmaxMintAmount) public onlyOwner() {
            maxMintAmount = _newmaxMintAmount;
        }
        
        function setBaseURI(string memory _newBaseURI) public onlyOwner() {
            baseURI = _newBaseURI;
        }
        
        function setBaseExtension(string memory _newBaseExtension) public onlyOwner() {
            baseExtension = _newBaseExtension;
        }
        //only owner Dracore Version
        //Set sorting address
        function setaddress1 (address _setaddres1) public onlyOwner() {
            address1 = _setaddres1;
        }
        
        function setaddress2 (address _setaddres2) public onlyOwner() {
            address2 = _setaddres2;
        }

        function setaddress3 (address _setaddres3) public onlyOwner() {
            address3 = _setaddres3;
        }

        function setaddress4 (address _setaddres4) public onlyOwner() {
            address4 = _setaddres4;
        }

        function setliquidityadd (address _setliquidityadd) public onlyOwner() {
            liquidity = _setliquidityadd;
        }

        function setmarketAdvSecurity (address _setmarketadvsecurity) public onlyOwner() {
            marketAdvSecurity = _setmarketadvsecurity;
        }

        function setdevelopment (address _setdevelopment) public onlyOwner() {
            development = _setdevelopment;
        }

        function setlegal (address _setlegal) public onlyOwner() {
            legal = _setlegal;
        }

        //set Cost and Fcost
        function setcost(uint256 _setcost) public onlyOwner() {
            cost = _setcost;
        }

        function setFcost(uint256 _setFcost) public onlyOwner() {
            Fcost = _setFcost;
        }
        
        //set Percentage
        function setFriendP(uint8 _percentage) public onlyOwner {
             require(_percentage <= 100);
             friendP = _percentage;
        }

        function setpercentageadd1(uint8 _percentageadd1) public onlyOwner {
             require(_percentageadd1 <= 100);
             address1P = _percentageadd1;
        }

        function setpercentageadd2(uint8 _percentageadd2) public onlyOwner {
             require(_percentageadd2 <= 100);
             address2P = _percentageadd2;
        }

        function setpercentageadd3(uint8 _percentageadd3) public onlyOwner {
             require(_percentageadd3 <= 100);
             address3P = _percentageadd3;
        }

        function setpercentageadd4(uint8 _percentageadd4) public onlyOwner {
             require(_percentageadd4 <= 100);
             address4P = _percentageadd4;
        }

        function setpercentliquidity(uint8 _percentageliquidity) public onlyOwner {
             require(_percentageliquidity <= 100);
             liquidityP = _percentageliquidity;
        }

        function setpercentageMarketadv(uint8 _percentagemarketAdv) public onlyOwner {
             require(_percentagemarketAdv <= 100);
             marketAdvSecurityP = _percentagemarketAdv;
        }

        function setpercentagedevelopment(uint8 _percentagedevelopment) public onlyOwner {
             require(_percentagedevelopment <= 100);
             developmentP = _percentagedevelopment;
        }

        function setpercentagelegal(uint8 _percentagelegal) public onlyOwner {
             require(_percentagelegal <= 100);
             legalP = _percentagelegal;
        }

        function setmintpermit(uint256 _setmintpermit) public onlyOwner {
               mintPermit = _setmintpermit;
        }

        function pause(bool _state) public onlyOwner() {
            paused = _state;
        }
        
        function withdraw() public payable onlyOwner() {
            require(payable(msg.sender).send(address(this).balance));
        }
}

