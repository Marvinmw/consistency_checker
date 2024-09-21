## whitepaper

### Item v1

   &ensp;**info**
   &emsp; 
- Description: 
    8.5% AUTOMATIC DISTRIBUTION
    When you buy the token, you are added to a list of people that are subject to redistributions.
    The contract, on each transaction, handles redistributions to a few of the addresses
    on the list, on a first-to-last basis. Once it goes through the whole list, it starts again. This means your reflections are always in a “queue” until they are released.
     
   - Possible Var Names from ChatGPT: ['redistributionFee', 'reflectionQueueFee', 'automaticDistributionFee'] 
   - Expression:  0.085 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    reflectionFee

   &ensp;**matched_var_exp**
    reflectionFee = 850

   &ensp;**isEq**
    True

### Item v2

   &ensp;**info**
   &emsp; 
- Description: 
    2.0% LIQUIDITY GENERATION
    2% of all transactions will deposit into the liquidity pool to elevate it. This sustains the life of the token.
     
   - Possible Var Names from ChatGPT: ['liquidityGenerationFee', 'liquidityPoolFee', 'tokenSustainabilityFee'] 
   - Expression:  0.02 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = 200

   &ensp;**isEq**
    True

### Item v3

   &ensp;**info**
   &emsp; 
- Description: 
    4% BUYBACK ACCUMULATION
    4% of all transactions are added to a buyback wallet. This wallet performs buybacks manually in the form of “MoonShot” and “AutoBoost.” All buyback tokens are burned.
     
   - Possible Var Names from ChatGPT: ['buybackFee', 'buybackAccumulation', 'buybackWallet'] 
   - Expression:  0.04 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    buybackFee

   &ensp;**matched_var_exp**
    buybackFee = 400

   &ensp;**isEq**
    True

### Item v4

   &ensp;**info**
   &emsp; 
- Description: 
    1.5% of all transactions is distributed to our marketing wallet. These tokens are LOCKED and vested weekly to the team.
     
   - Possible Var Names from ChatGPT: ['marketingFee', 'lockedTokensVested', 'weeklyTeamVesting'] 
   - Expression:  0.015 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    marketingFee

   &ensp;**matched_var_exp**
    marketingFee = 150

   &ensp;**isEq**
    True

### Item v5

   &ensp;**info**
   &emsp; 
- Description: 
    ANTI-WHALE
    The anti-whale mechanic disallows sellers to offload more than 0.1% of the entire supply of the token. This prevents coordinated dumping of tokens and encourages long-term holding
     
   - Possible Var Names from ChatGPT: ['whaleFeeThreshold', 'maxDumpPercentage', 'longTermHoldLimit'] 
   - Expression:  totalSupply * 0.001 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    swapThreshold

   &ensp;**matched_var_exp**
    swapThreshold = _totalSupply / 1000

   &ensp;**isEq**
    True


## hidden_fee_function

### shouldTakeFee

  &ensp;** Possible Values **:
 ~isFeeExempt_sender_ & ~isWhiteList_recipient_ & ~isWhiteList_sender_

### getTotalFee

  &ensp;** Possible Values **:
 9999, 
 1600, 
 160*buybackMultiplierTriggeredAt/3 - 160*timestamp/3 + 3200, 
 2880, 
 1600

### getMultipliedFee

  &ensp;** Possible Values **:
 2880, 
 160*buybackMultiplierTriggeredAt/3 - 160*timestamp/3 + 3200, 
 1600


## hidden_fee_var

### feeIncrease

  &ensp;** Possible Values **:
 1600

### feeAmount

  &ensp;** Possible Values **:
 4*amount/25, 
 36*amount/125, 
 2*amount*(buybackMultiplierTriggeredAt - timestamp + 60)/375, 
 4*amount/25, 
 9999*amount/10000

### dynamicLiquidityFee_0

  &ensp;** Possible Values **:
 0

### dynamicLiquidityFee_1

  &ensp;** Possible Values **:
 200

### totalBNBFee

  &ensp;** Possible Values **:
 1600 - dynamicLiquidityFee/2

### isFeeExempt_holder_

  &ensp;** Possible Values **:
 exempt

### liquidityFee

  &ensp;** Possible Values **:
 _liquidityFee

### buybackFee

  &ensp;** Possible Values **:
 _buybackFee

### reflectionFee

  &ensp;** Possible Values **:
 _reflectionFee

### marketingFee

  &ensp;** Possible Values **:
 _marketingFee

### totalFee

  &ensp;** Possible Values **:
 _buybackFee + _liquidityFee + _marketingFee + _reflectionFee

### feeDenominator

  &ensp;** Possible Values **:
 _feeDenominator

### marketingFeeReceiver

  &ensp;** Possible Values **:
 _marketingFeeReceiver


