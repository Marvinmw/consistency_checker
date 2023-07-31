## whitepaper

### Item v0

   &ensp;**info**
   &emsp; 
- Description: 
    Buy tax 7%
     
   - Possible Var Names from ChatGPT: ['buyTax', 'purchaseTax', 'acquisitionTax'] 
   - Expression:  0.07 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    previousSellRewardsFee

   &ensp;**matched_var_exp**
    previousSellRewardsFee = sellRewardsFee

   &ensp;**isEq**
    Eq(sellRewardsFee, 7.0)

### Item v1

   &ensp;**info**
   &emsp; 
- Description: 
    Buy marketing 6%
     
   - Possible Var Names from ChatGPT: ['marketingBuyFee', 'buyFeeMarketing', 'chargePercentBuyMarketing'] 
   - Expression:  0.06 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    buyMarketingFee

   &ensp;**matched_var_exp**
    buyMarketingFee = 7

   &ensp;**isEq**
    False

### Item v2

   &ensp;**info**
   &emsp; 
- Description: 
   Buy rewards 0% buy back and burn
     
   - Possible Var Names from ChatGPT: ['rewardBuybackBurnFee', 'buyRewardFee', 'rewardChargePercent'] 
   - Expression:  0.00 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    buyRewardsFee

   &ensp;**matched_var_exp**
    buyRewardsFee = 6

   &ensp;**isEq**
    False

### Item v3

   &ensp;**info**
   &emsp; 
- Description: 
    Sell tax 7%  
     
   - Possible Var Names from ChatGPT: ['sellTax', 'salesTax', 'disposalTax'] 
   - Expression:  0.07 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    sellMarketingFee

   &ensp;**matched_var_exp**
    sellMarketingFee = 7

   &ensp;**isEq**
    True

### Item v4

   &ensp;**info**
   &emsp; 
- Description: 
   Sell marketing 4% 
     
   - Possible Var Names from ChatGPT: ['marketingSellFee', 'sellFeeMarketing', 'chargePercentSellMarketing'] 
   - Expression:  0.04 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    sellMarketingFee

   &ensp;**matched_var_exp**
    sellMarketingFee = 7

   &ensp;**isEq**
    False

### Item v5

   &ensp;**info**
   &emsp; 
- Description: 
    Sell buy back and burn 6%
     
   - Possible Var Names from ChatGPT: ['sellBuybackBurnFee', 'buybackBurnSellFee', 'chargePercentSellBuybackBurn'] 
   - Expression:  0.06 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    sellBuyBackFee

   &ensp;**matched_var_exp**
    sellBuyBackFee = 4

   &ensp;**isEq**
    False

### Item v6

   &ensp;**info**
   &emsp; 
- Description: 
    max wallet size (each wallet can only hold 1.5% of supply). 
     
   - Possible Var Names from ChatGPT: ['maxWalletSize', 'walletLimit', 'supplyThreshold'] 
   - Expression:  0.015 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    rewardsWallet

   &ensp;**matched_var_exp**
    rewardsWallet = 0x83aF9cd324b20D767179F47F00e59E83d1eaaC99

   &ensp;**isEq**
    False


## hidden_fee_function

### getIsExcludedFromFees

  &ensp;** Possible Values **:
 isExcludedFromFees_account_


## hidden_fee_var

### isExcludedFromFees__presaleAddress_

  &ensp;** Possible Values **:
 True

### isExcludedFromFees__partnerOrExchangeAddress_

  &ensp;** Possible Values **:
 True

### isExcludedFromFees__newWallet_

  &ensp;** Possible Values **:
 True

### transferFeeIncreaseFactor

  &ensp;** Possible Values **:
 _multiplier

### buyRewardsFee

  &ensp;** Possible Values **:
 0, 
 6, 
 0, 
 previousBuyRewardsFee, 
 _buyRewardsFee

### buyMarketingFee

  &ensp;** Possible Values **:
 0, 
 7, 
 0, 
 previousBuyMarketingFee, 
 _buyMarketingFee

### buyBuyBackFee

  &ensp;** Possible Values **:
 0, 
 0, 
 0, 
 previousBuyBuyBackFee, 
 _buyBuyBackFee

### sellRewardsFee

  &ensp;** Possible Values **:
 0, 
 6, 
 0, 
 previousSellRewardsFee, 
 _sellRewardsFee

### sellMarketingFee

  &ensp;** Possible Values **:
 0, 
 7, 
 0, 
 previousSellMarketingFee, 
 _sellMarketingFee

### sellBuyBackFee

  &ensp;** Possible Values **:
 0, 
 4, 
 0, 
 previousSellBuyBackFee, 
 _sellBuyBackFee

### totalBuyFees

  &ensp;** Possible Values **:
 13, 
 13, 
 13, 
 buyBuyBackFee + 7, 
 buyBuyBackFee + 7, 
 buyBuyBackFee + 6, 
 buyBuyBackFee + 6, 
 buyBuyBackFee + 13

### totalSellFees

  &ensp;** Possible Values **:
 17, 
 13, 
 13, 
 11, 
 11, 
 10, 
 10, 
 17

### botFees

  &ensp;** Possible Values **:
 _botFees, 
 percent

### previousBuyBuyBackFee

  &ensp;** Possible Values **:
 0

### previousSellBuyBackFee

  &ensp;** Possible Values **:
 0

### previousBuyRewardsFee

  &ensp;** Possible Values **:
 0

### previousSellRewardsFee

  &ensp;** Possible Values **:
 0

### previousBuyMarketingFee

  &ensp;** Possible Values **:
 0

### previousSellMarketingFee

  &ensp;** Possible Values **:
 0

### isExcludedFromFees_account_

  &ensp;** Possible Values **:
 excluded

### fees

  &ensp;** Possible Values **:
 amount*totalBuyFees/100, 
 fees - rewardPortion, 
 amount*totalSellFees/100, 
 fees - rewardPortion, 
 amount*totalTransferFees/100, 
 fees - rewardPortion, 
 amount*botFees/100

### takeFee

  &ensp;** Possible Values **:
 False

### totalTransferFees

  &ensp;** Possible Values **:
 totalSellFees


