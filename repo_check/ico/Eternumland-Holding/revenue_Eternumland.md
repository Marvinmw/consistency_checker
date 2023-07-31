## whitepaper

### Item v0

   &ensp;**info**
   &emsp; 
- Description: 
    10% Friend Code. 
     
   - Possible Var Names from ChatGPT: ['friendCodeFee', 'referralCharge', 'discountPercent'] 
   - Expression:  0.01 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    maxMintAmount

   &ensp;**matched_var_exp**
    maxMintAmount = 50

   &ensp;**isEq**
    False

### Item v1

   &ensp;**info**
   &emsp; 
- Description: 
    10% Discount with Friend Code
     
   - Possible Var Names from ChatGPT: ['friendCodeDiscount', 'referralDiscount', 'discountWithCode'] 
   - Expression:  0.01 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    liquidity

   &ensp;**matched_var_exp**
    liquidity = _setliquidityadd

   &ensp;**isEq**
    Eq(_setliquidityadd, 0.01)

### Item v2

   &ensp;**info**
   &emsp; 
- Description: 
   16%  Marketing,  on  social  channels  and  platforms  dedicated  to  publicizing Blockchain projects
     
   - Possible Var Names from ChatGPT: ['socialMediaMarketingFee', 'blockchainPublicityCharge', 'marketingPlatformFee'] 
   - Expression:  0.16 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    marketAdvSecurity

   &ensp;**matched_var_exp**
    marketAdvSecurity = _setmarketadvsecurity

   &ensp;**isEq**
    Eq(_setmarketadvsecurity, 16.0)

### Item v3

   &ensp;**info**
   &emsp; 
- Description: 
    8% Security: Blockchain security systems, To provide users with  increasing security. This item will always be reported in different percentages each year.
     
   - Possible Var Names from ChatGPT: ['blockchainSecurityFee', 'userProtectionCharge', 'securitySystemCost'] 
   - Expression:  0.08 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    marketAdvSecurity

   &ensp;**matched_var_exp**
    marketAdvSecurity = _setmarketadvsecurity

   &ensp;**isEq**
    Eq(_setmarketadvsecurity, 8.0)

### Item v4

   &ensp;**info**
   &emsp; 
- Description: 
   18%  Corporate  incorporation,  opening  of  Eternumland  Holding and acquisition of the first funeral home run by staff already on the  Team  and  already  trained  to  the  founder's  high  and  ethical standards.
     
   - Possible Var Names from ChatGPT: ['incorporationFee', 'funeralHomeAcquisitionCost', 'ethicalTrainingExpense'] 
   - Expression:  0.18 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    liquidity

   &ensp;**matched_var_exp**
    liquidity = _setliquidityadd

   &ensp;**isEq**
    Eq(_setliquidityadd, 18.0)

### Item v5

   &ensp;**info**
   &emsp; 
- Description: 
    15%  Liquidity  ETRN,  this  slice  from  the  sale  of  NFTs  will  be allocated  to  Token  Liquidity  and  will  be  used  at  the  end  of  the "Token Sale" ETRN.
     
   - Possible Var Names from ChatGPT: ['ETRNLiquidityFee', 'tokenSaleLiquidityCharge', 'NFTSaleLiquidityAllocation'] 
   - Expression:  0.15 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    liquidityP

   &ensp;**matched_var_exp**
    liquidityP = 15

   &ensp;**isEq**
    True

### Item v6

   &ensp;**info**
   &emsp; 
- Description: 
    8% Team, intended for all members and vendors working on the project.
     
   - Possible Var Names from ChatGPT: ['teamFee', 'vendorCharge', 'projectCompensationCost'] 
   - Expression:  0.08 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    cost

   &ensp;**matched_var_exp**
    cost = 800000000000000000

   &ensp;**isEq**
    False

### Item v7

   &ensp;**info**
   &emsp; 
- Description: 
8%  Development,  these  funds  are  dedicated  to  improving  the graphical UI, developing new smart contracts to unite companies, and building the DAO.
 
   - Possible Var Names from ChatGPT: ['developmentFee', 'UIImprovementCost', 'smartContractR&DCharge'] 
   - Expression:  0.08 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    cost

   &ensp;**matched_var_exp**
    cost = 800000000000000000

   &ensp;**isEq**
    False

### Item v8

   &ensp;**info**
   &emsp; 
- Description: 
7% Advisors, Tax Advisors and Blockchain.
 
   - Possible Var Names from ChatGPT: ['advisorFee', 'taxConsultantCharge', 'blockchainExpertExpense'] 
   - Expression:  0.07 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    mintPermit

   &ensp;**matched_var_exp**
    mintPermit = _setmintpermit

   &ensp;**isEq**
    Eq(_setmintpermit, 7.0)


## hidden_fee_function


## hidden_fee_var


