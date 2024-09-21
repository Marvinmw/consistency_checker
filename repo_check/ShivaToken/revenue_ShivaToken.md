## whitepaper

### Item v0

   &ensp;**info**
   &emsp; 
- Description: 
    Reflection Rate: 10% of every transaction is AUTOMATICALLY redistributed to the holders in $BTCB Bitcoin.
     
   - Possible Var Names from ChatGPT: ['reflectionRateBTCB', 'redistributionFeeBTCB', 'holderRedistributionRate'] 
   - Expression:  0.1 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    BTCBRewardsFee

   &ensp;**matched_var_exp**
    BTCBRewardsFee = 10

   &ensp;**isEq**
    True

### Item v1

   &ensp;**info**
   &emsp; 
- Description: 
    Marketing Tax Rate: The marketing wallet will receive 5% tax as BNB from the transactions.
     
   - Possible Var Names from ChatGPT: ['marketingTaxRate', 'marketingFeePercentage', 'marketingBNBTax'] 
   - Expression:  0.05 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    marketingFee

   &ensp;**matched_var_exp**
    marketingFee = 5

   &ensp;**isEq**
    True

### Item v2

   &ensp;**info**
   &emsp; 
- Description: 
    Automatic Liquidity Rate: 3% of every transaction contributes toward automatically generating liquidity on PancakeSwap.
     
   - Possible Var Names from ChatGPT: ['liquidityRate', 'automaticLiquidityFee', 'pancakeSwapLiquidityContribution'] 
   - Expression:  0.03 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = 3

   &ensp;**isEq**
    True

### Item v3

   &ensp;**info**
   &emsp; 
- Description: 
    Auto Buy-back Burn: 5% tax from every sell transaction will be used for Buy back-Token and Burn it.
     
   - Possible Var Names from ChatGPT: ['autoBuybackBurnFee', 'sellTransactionFee', 'buybackBurnTax'] 
   - Expression:  0.05 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    marketingFee

   &ensp;**matched_var_exp**
    marketingFee = 5

   &ensp;**isEq**
    True

### Item v4

   &ensp;**info**
   &emsp; 
- Description: 
    After a certain amount of tokens have been stored in the contract (0.0001% of the total supply) it initiates a swap.
     
   - Possible Var Names from ChatGPT: ['feeThreshold', 'tokenSwapTrigger', 'chargeInitiationAmount'] 
   - Expression:  0.000001 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    limitSwap

   &ensp;**matched_var_exp**
    limitSwap = true

   &ensp;**isEq**
    False

### Item v4_

   &ensp;**info**
   &emsp; 
- Description: 
    After a certain amount of tokens have been stored in the contract (0.0001% of the total supply) it initiates a swap.
     
   - Possible Var Names from ChatGPT: ['feeThreshold', 'tokenSwapTrigger', 'chargeInitiationAmount'] 
   - Expression:  0.000001*totaolSupply 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    limitSwap

   &ensp;**matched_var_exp**
    limitSwap = true

   &ensp;**isEq**
    False

### Item v5

   &ensp;**info**
   &emsp; 
- Description: 
   Each owner of Shiva tokens is eligible to automatically receive $BTCB from the reward pool. The reward pool contains a number of $BTCB tokens reserved by the contract. The contract uses a portion of the tax applied to every transaction (10%) to do this.
     
   - Possible Var Names from ChatGPT: ['rewardPoolBTCB', 'tokenRewardFee', 'btcbRewardShare'] 
   - Expression:  0.1 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    BTCBRewardsFee

   &ensp;**matched_var_exp**
    BTCBRewardsFee = 10

   &ensp;**isEq**
    True

### Item v6

   &ensp;**info**
   &emsp; 
- Description: 
    After a certain amount of tokens are stored in the contract (20,000,000 Token) it initiates a swap. A swap in this context is the process of swapping the contract's token balance with $BTCBs in order to increase the reward pool. 
     
   - Possible Var Names from ChatGPT: ['tokenSwapThreshold', 'feeSwapThreshold', 'rewardPoolBoostThreshold'] 
   - Expression:  20000000 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    limitSwap

   &ensp;**matched_var_exp**
    limitSwap = true

   &ensp;**isEq**
    False

### Item v7

   &ensp;**info**
   &emsp; 
- Description: 
    The SHIVA token will be created with 51 Billion Supply.
     
   - Possible Var Names from ChatGPT: ['shivaTokenSupply', 'shivaTokenTotal', 'shivaTokenAmount'] 
   - Expression:  51000000000 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    swapTokensAtAmount

   &ensp;**matched_var_exp**
    swapTokensAtAmount = 20000000 * ( 10 ** 18 )

   &ensp;**isEq**
    False


## hidden_fee_function

### isExcludedFromFees

  &ensp;** Possible Values **:
 _isExcludedFromFees_account_


## hidden_fee_var

### _isExcludedFromFees_account_

  &ensp;** Possible Values **:
 excluded

### _isExcludedFromFees [ accounts_i_]

  &ensp;** Possible Values **:
 excluded

### maxTransferAmountRate

  &ensp;** Possible Values **:
 _maxTransferAmountRate

### BTCBRewardsFee

  &ensp;** Possible Values **:
 value

### totalFees

  &ensp;** Possible Values **:
 18, 
 18, 
 18

### liquidityFee

  &ensp;** Possible Values **:
 value

### marketingFee

  &ensp;** Possible Values **:
 value


