## whitepaper

### Item v0

   &ensp;**info**
   &emsp; 
- Description: 
    Total Transfer Tax Rate: 2% of every transfer
     
   - Possible Var Names from ChatGPT: ['transferTaxRate', 'totalTransferTax', 'transferFee'] 
   - Expression:  0.02 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    transferTaxRate

   &ensp;**matched_var_exp**
    transferTaxRate = 500

   &ensp;**isEq**
    False

### Item v1

   &ensp;**info**
   &emsp; 
- Description: 
    Automatic Liquidity
    the PANTHER-BNB liquidity pool through the contract automatically. 
     
   - Possible Var Names from ChatGPT: ['autoLiquidityFee', 'liquidityCharge', 'liquidityPoolFee'] 
   - Expression:  0.01 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    referralCommissionRate

   &ensp;**matched_var_exp**
    referralCommissionRate = 100

   &ensp;**isEq**
    True

### Item v2

   &ensp;**info**
   &emsp; 
- Description: 
    Automatic Burning
    According to our tokenomics design, each transfer must pay a 2% transfer tax. The 1% transfer tax will be burned (sent to the black hole address) immediately.
     
   - Possible Var Names from ChatGPT: ['transferTaxBurn', 'automaticBurningFee', 'tokenomicsTransferTax'] 
   - Expression:  0.01 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    transferTaxRate

   &ensp;**matched_var_exp**
    transferTaxRate = 500

   &ensp;**isEq**
    False

### Item v3

   &ensp;**info**
   &emsp; 
- Description: 
    Anti Whale
    Transfer more than 0.15% (current ratio) of the total supply will be rejected. As the total supply grows, this ratio will be reduced.
    Deposit or withdraw tokens to the farms will not be subject to this restriction.
     
   - Possible Var Names from ChatGPT: ['antiWhaleFeeRatio', 'transferRestrictionRatio', 'restrictedTransferFee'] 
   - Expression:  0.0015 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    maxTransferAmountRate

   &ensp;**matched_var_exp**
    maxTransferAmountRate = 50

   &ensp;**isEq**
    False

### Item v4

   &ensp;**info**
   &emsp; 
- Description: 
    Deposit Fee Redistribution
    Deposit Fee
    When users enter the farming on PantherSwap, a 4% deposit fee will be charged. 
    1% deposit fee will be sent to the dev team as the development fund.
    3% deposit fee will be redistributed to PANTHER holders via Jungles farming.
     
   - Possible Var Names from ChatGPT: ['depositFee', 'devFundFee', 'redistributionFee'] 
   - Expression:  0.04 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    referralCommissionRate

   &ensp;**matched_var_exp**
    referralCommissionRate = 100

   &ensp;**isEq**
    False

### Item v5

   &ensp;**info**
   &emsp; 
- Description: 
    Referral Program
    An on-chain referral program has been implemented to incentivize users to invite friends to join the farming. Inviters can earn 1% of his/her friends' earnings forever.
    Visit PantherSwap referral program page: https://pantherswap.com/referrals​
    Unlock your wallet to get your unique referral link
    Share your referral link with your friends
    Every time your friends get rewards from farms, you will receive referral commissions automatically
    The current referral commission rate is 1%
     
   - Possible Var Names from ChatGPT: ['referralCommissionRate', 'referralLink', 'inviteeEarningsPercentage'] 
   - Expression:  0.01 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    referralCommissionRate

   &ensp;**matched_var_exp**
    referralCommissionRate = 100

   &ensp;**isEq**
    True


## hidden_fee_function


## hidden_fee_var

### burnRate

  &ensp;** Possible Values **:
 _burnRate


