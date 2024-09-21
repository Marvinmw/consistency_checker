## whitepaper

### Item v0

   &ensp;**info**
   &emsp; 
- Description: 
    ENIX is an BEP20 token on the Binance Smart Chain, with a maximum supply of 500,000,000 tokens.
     
   - Possible Var Names from ChatGPT: ['ENIX_MAX_SUPPLY', 'TOKEN_MAX_SUPPLY', 'BEP20_MAX_SUPPLY'] 
   - Expression:  500000000 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    _rTotal

   &ensp;**matched_var_exp**
    _rTotal = ( MAX - ( MAX % _tTotal ) )

   &ensp;**isEq**
    Eq(MAX - Mod(MAX, _tTotal), 500000000000000000000000000)

### Item v0_

   &ensp;**info**
   &emsp; 
- Description: 
    ENIX is an BEP20 token on the Binance Smart Chain, with a maximum supply of 500,000,000 tokens.
     
   - Possible Var Names from ChatGPT: ['ENIX_MAX_SUPPLY', 'TOKEN_MAX_SUPPLY', 'BEP20_MAX_SUPPLY'] 
   - Expression:  500000000*10 ** 18 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    _rTotal

   &ensp;**matched_var_exp**
    _rTotal = ( MAX - ( MAX % _tTotal ) )

   &ensp;**isEq**
    Eq(MAX - Mod(MAX, _tTotal), 500000000000000000000000000)

### Item v1

   &ensp;**info**
   &emsp; 
- Description: 
    Every trade contributes 3% to the liquidity pool, resulting in a growing price floor and a sustainable token.
     
   - Possible Var Names from ChatGPT: ['liquidityFee', 'tradeContributionFee', 'sustainableTokenFee'] 
   - Expression:  0.03 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    liquidityFeeonBuy

   &ensp;**matched_var_exp**
    liquidityFeeonBuy = 3

   &ensp;**isEq**
    True

### Item v2

   &ensp;**info**
   &emsp; 
- Description: 
   2% of every buy and sell transaction is divided among all present holders in proportion to their holdings. 
     
   - Possible Var Names from ChatGPT: ['distributionFee', 'proportionalFee', 'transactionReward'] 
   - Expression:  0.02 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    MarketingFee

   &ensp;**matched_var_exp**
    MarketingFee = 2

   &ensp;**isEq**
    True

### Item v3

   &ensp;**info**
   &emsp; 
- Description: 
    4% of all transactions are automatically transferred to the Development/ Research wallet. 
     
   - Possible Var Names from ChatGPT: ['developmentFee', 'researchWalletFee', 'transactionAllocation'] 
   - Expression:  0.04 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    holdersFee

   &ensp;**matched_var_exp**
    holdersFee = 2

   &ensp;**isEq**
    False

### Item v4

   &ensp;**info**
   &emsp; 
- Description: 
   To establish deflationary conditions for the token, 2.5% (12,500,000 tokens) were sent to a burn address (0x000) immediately after the contract was deployed. 
     
   - Possible Var Names from ChatGPT: ['burnFee', 'deflationaryAllocation', 'initialTokenBurn'] 
   - Expression:  0.025 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    holdersFee

   &ensp;**matched_var_exp**
    holdersFee = 2

   &ensp;**isEq**
    False

### Item v5

   &ensp;**info**
   &emsp; 
- Description: 
  More ENIX tokens will be burned at various points in the future until 15% of the total supply has been burned.
     
   - Possible Var Names from ChatGPT: ['futureBurn', 'supplyReduction', 'ongoingTokenBurn'] 
   - Expression:  0.15 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    swapTokensAtAmount

   &ensp;**matched_var_exp**
    swapTokensAtAmount = _tTotal / 5000

   &ensp;**isEq**
    Eq(_tTotal/5000, 15.0)


## hidden_fee_function

### _getRate

  &ensp;** Possible Values **:
 _rTotal/_tTotal

### calculateTaxFee

  &ensp;** Possible Values **:
 _amount*_taxFee/100

### calculateLiquidityFee

  &ensp;** Possible Values **:
 _amount*_liquidityFee/100

### calculateBurnFee

  &ensp;** Possible Values **:
 _amount*_burnFee/100

### isExcludedFromFee

  &ensp;** Possible Values **:
 _isExcludedFromFees_account_


## hidden_fee_var

### _tFeeTotal

  &ensp;** Possible Values **:
 _tFeeTotal + tAmount, 
 _tFeeTotal + tFee

### currentRate

  &ensp;** Possible Values **:
 _rTotal/_tTotal, 
 _rTotal/_tTotal, 
 _rTotal/_tTotal

### tFee

  &ensp;** Possible Values **:
 _amount*_taxFee/100, 
 _amount*_taxFee/100, 
 _amount*_taxFee/100, 
 _amount*_taxFee/100, 
 _amount*_taxFee/100, 
 _amount*_taxFee/100

### rFee

  &ensp;** Possible Values **:
 currentRate*tFee, 
 currentRate*tFee, 
 currentRate*tFee, 
 currentRate*tFee, 
 currentRate*tFee, 
 currentRate*tFee

### _taxFee

  &ensp;** Possible Values **:
 0, 
 11, 
 4

### _burnFee

  &ensp;** Possible Values **:
 0, 
 0, 
 0

### _liquidityFee

  &ensp;** Possible Values **:
 0, 
 3, 
 3

### _isExcludedFromFees_account_

  &ensp;** Possible Values **:
 excluded


