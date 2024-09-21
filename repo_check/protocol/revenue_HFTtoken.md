## whitepaper

### Item v0

   &ensp;**info**
   &emsp; 
- Description: 
    Reflection (2%)
    What is reflection?
    Reflection, as many people know it, is often used by meme coins.
    The Hodl Finance team sees reflection as an advanced smart contract mechanism to easily reward the community for holding on to HFT. No need for complex smart contract interactions like staking, liquidity providing or yield farming.
     
   - Possible Var Names from ChatGPT: ['reflectionFee', 'hodlReward', 'communityReward'] 
   - Expression:  0.02 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    reflectionFee

   &ensp;**matched_var_exp**
    reflectionFee = 2

   &ensp;**isEq**
    True

### Item v1

   &ensp;**info**
   &emsp; 
- Description: 
    Liquidity Pool (1%)
    What is a liquidity Pool?
    A liquidity pool is a collection of funds locked in a smart contract making a token tradable on decentralized exchanges. 
    A liquidity pool consists of two different tokens both representing a certain value which combined are known as 'the liquidity'. Most of the time a liquidity pool is created with 50% of a certain token on one side and 50% of the other token on the other side.
    When liquidity is provided to a liquidity pool, people receive liquidity pool tokens which serve as their evidence in the blockchain proving that they provided this liquidity.
     
   - Possible Var Names from ChatGPT: ['liquidityPoolFee', 'liquidityCharge', 'liquidityFeePercentage'] 
   - Expression:  0.01 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = 2

   &ensp;**isEq**
    False

### Item v2

   &ensp;**info**
   &emsp; 
- Description: 
    threshold for the HFT liquidity pool
    We anticipated on that by implementing a threshold of 2200 BNB for the HFT liquidity pool as we determined this to be the perfect balance between enough liquidity and tradable volatility. 
    Once the threshold of 2200 BNB is met, the part of the network fee which goes to the liquidity pool will flow to the marketing treasury.
     
   - Possible Var Names from ChatGPT: ['hftLiquidityPoolThreshold', 'liquidityThreshold', 'bnbThreshold'] 
   - Expression:  2200 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    previousLiquidityFee

   &ensp;**matched_var_exp**
    previousLiquidityFee = liquidityFee

   &ensp;**isEq**
    Eq(liquidityFee, 2200000000000000000000)

### Item v3

   &ensp;**info**
   &emsp; 
- Description: 
    Foundation (3%)
    What is the foundation?
    The foundation is the entity making sure all operations on the central side of the Hodl Finance ecosystem run smoothly. It manages the manual conversions, buy-backs with profits, and last but certainly not least the Foundation Trading Algorithms (FTA), which serve as the core engine of the total ecosystem. 
     
   - Possible Var Names from ChatGPT: ['foundationFee', 'foundationCharge', 'foundationPercentage'] 
   - Expression:  0.03 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    foundationFee

   &ensp;**matched_var_exp**
    foundationFee = 6

   &ensp;**isEq**
    False

### Item v4

   &ensp;**info**
   &emsp; 
- Description: 
    Marketing treasury (3%)
    What is the marketing treasury?
    The marketing treasury has been implemented after proposal 001 was approved by the community. It will be used for all marketing related actions so that the word of Hodl Finance will be spread. Same as for Reflection and Foundation, the smart contracts automatically send 3 percent out of the 10 percent Network fee to the Marketing treasury.
     
   - Possible Var Names from ChatGPT: ['marketingTreasuryFee', 'marketingFee', 'spreadFee'] 
   - Expression:  0.03 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    foundationFee

   &ensp;**matched_var_exp**
    foundationFee = 6

   &ensp;**isEq**
    False

### Item v5

   &ensp;**info**
   &emsp; 
- Description: 
    Mystery challenge (1%)
    Be extraordinary if you want to stand out
    We can not say much about the mystery challenge yet, but it will be something else. Something that has never been done in the crypto domain before.
     
   - Possible Var Names from ChatGPT: ['mysteryChallengeFee', 'extraordinaryFee', 'uniqueCryptoFee'] 
   - Expression:  0.01 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = 2

   &ensp;**isEq**
    False


## hidden_fee_function

### totalFees

  &ensp;** Possible Values **:
 tFeeTotal

### _getRate

  &ensp;** Possible Values **:
 rTotal/T_TOTAL

### getExcludedFromFee

  &ensp;** Possible Values **:
 isExcludedFromFee__account_


## hidden_fee_var

### isExcludedFromFee_address_this_

  &ensp;** Possible Values **:
 True

### isExcludedFromFee_WALLET_TREASURY_

  &ensp;** Possible Values **:
 True

### isExcludedFromFee_WALLET_AIRDROP_

  &ensp;** Possible Values **:
 True

### isExcludedFromFee_WALLET_LP_SUPPLY_

  &ensp;** Possible Values **:
 True

### isExcludedFromFee_WALLET_DEV_

  &ensp;** Possible Values **:
 True

### isExcludedFromFee_WALLET_ADVISORS_

  &ensp;** Possible Values **:
 True

### isExcludedFromFee_WALLET_TEAM_

  &ensp;** Possible Values **:
 True

### previousReflectionFee

  &ensp;** Possible Values **:
 0

### previousLiquidityFee

  &ensp;** Possible Values **:
 0

### previousFoundationFee

  &ensp;** Possible Values **:
 0

### reflectionFee

  &ensp;** Possible Values **:
 0, 
 previousReflectionFee

### liquidityFee

  &ensp;** Possible Values **:
 0, 
 previousLiquidityFee

### foundationFee

  &ensp;** Possible Values **:
 0, 
 previousFoundationFee

### _takeFee

  &ensp;** Possible Values **:
 False, 
 True

### currentRate

  &ensp;** Possible Values **:
 rTotal/T_TOTAL

### tFeeTotal

  &ensp;** Possible Values **:
 _tFee + tFeeTotal


