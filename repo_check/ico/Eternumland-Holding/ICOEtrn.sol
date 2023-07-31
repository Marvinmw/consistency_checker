// SPDX-License-Identifier: MIT LICENSE

pragma solidity 0.8.4;

import "Etern.sol";

contract ICOEtern is Ownable {

uint256 cost1 = 150000000000000; //0.00015 BNB
uint256 cost2 = 200000000000000; //0.00020 BNB
uint256 cost3 = 300000000000000; //0.00030 BNB
uint256 start = 1685570400; // 01/06/2023 00:00:00 +0200 (CEST) 
uint256 time1 = 1688162399; // 30/06/2023 23:59:59 +0200 (CEST)
uint256 time2 = 1690840799; // 31/07/2023 23:59:59 +0200 (CEST)
uint256 time3 = 1693519199; // 31/08/2023 23:59:59 +0200 (CEST)
uint256 Tokpresale = 5000000000000000000000000; // 5.000.000 Token
uint256 TokPrivate = 6000000000000000000000000; // 6.000.000 Token
uint256 Tokpublic = 10000000000000000000000000; // 10.000.000 Token

event Minted(address owner, uint256 amount);

uint256 public Totalsup;
  uint256 public operation;
  
  struct OwnerOperations {
    uint256 ammount;
    uint48 timestamp;
    address owner;
    uint256 operationid;
  }

  
   mapping(uint256 => OwnerOperations) public Total; 
   

  Etern token;

     constructor(Etern _token) { 
   
    token = _token;
  }
//Pre-sale function
  
  function PresaleBuy (uint256 _ammount) external payable {
           
            uint256 Ammountbuy = _ammount;
            uint256 ammountcontrol = _ammount/1000000000000000000;
                   require (block.timestamp >= start, "The presale has yet to begin");
                   require (Totalsup + Ammountbuy <= Tokpresale, "Pre-sale tokens sold out"); 
                   require (block.timestamp <= time1,"Pre-sale token time ended"); 
                   require (msg.value >= ammountcontrol * cost1,"Value too low");        

        token.mint(msg.sender, _ammount);
        emit Minted(msg.sender, ammountcontrol);
        
        Totalsup += Ammountbuy;
        operation += 1;

        Total [operation] = OwnerOperations({
        owner: msg.sender,
        ammount: uint256(_ammount),
        timestamp: uint48(block.timestamp),
        operationid: uint256 (operation)
});
     
}
// Private Buy
function PrivateBuy (uint256 _ammount) external payable {
           
            uint256 Ammountbuy = _ammount;
            uint256 ammountcontrol = _ammount/1000000000000000000;
                   require (Totalsup >= Tokpresale || block.timestamp >= time1, "Not available");
                   require (Totalsup + Ammountbuy <= TokPrivate, "Private tokens sold out "); 
                   require (block.timestamp <= time2,"Private token time ended"); 
                   require (msg.value >= ammountcontrol * cost2,"Value too low");        

        token.mint(msg.sender, _ammount);
        emit Minted(msg.sender, ammountcontrol);
        
        Totalsup += Ammountbuy;
        operation += 1;

        Total [operation] = OwnerOperations({
        owner: msg.sender,
        ammount: uint256(_ammount),
        timestamp: uint48(block.timestamp),
        operationid: uint256 (operation)
});
     
}

// Public Buy
function PublicBuy (uint256 _ammount) external payable {
           
            uint256 Ammountbuy = _ammount;
            uint256 ammountcontrol = _ammount/1000000000000000000;
                   require (Totalsup >= TokPrivate || block.timestamp >= time2, "Not available");
                   require (Totalsup + Ammountbuy <= Tokpublic, "Public tokens sold out "); 
                   require (block.timestamp <= time3,"Public token time ended"); 
                   require (msg.value >= ammountcontrol * cost3,"Value too low");        

        token.mint(msg.sender, _ammount);
        emit Minted(msg.sender, ammountcontrol);
        
        Totalsup += Ammountbuy;
        operation += 1;

        Total [operation] = OwnerOperations({
        owner: msg.sender,
        ammount: uint256(_ammount),
        timestamp: uint48(block.timestamp),
        operationid: uint256 (operation)
});
     
}

function Owneroperation (address account) public view returns (uint256[] memory ownerOperation) {

    uint256 supply = Totalsup;
    uint256[] memory tmp = new uint256[](supply);

    uint256 index = 0;
    for(uint opId = 1; opId <= supply; opId++) {
      if (Total[opId].owner == account) {
        tmp[index] = Total[opId].operationid;
        index +=1;
      }
    }

    uint256[] memory tokens = new uint256[](index);
    for(uint i = 0; i < index; i++) {
      tokens[i] = tmp[i];
    }

    return tokens;
  }
          
  function withdraw() public payable onlyOwner() {
            require(payable(msg.sender).send(address(this).balance));
        }  
              
   }



