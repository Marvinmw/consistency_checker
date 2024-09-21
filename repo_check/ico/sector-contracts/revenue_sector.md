## whitepaper

### Item v0

   &ensp;**info**
 '  &emsp; 
- Description: The total supply of $SECT tokens is fixed at 100 million, and no more tokens will be created in the future. 
   - Possible Var Names from ChatGPT: ['SECT_TOTAL_SUPPLY', 'MAX_SECT_TOKENS', 'SECT_FIXED_SUPPLY'] 
   - Expression:  100000000 
'

   &ensp;**Is the fee found**
 '   No'

   &ensp;**matched_var_name**
 '   MAX_STRATS'

   &ensp;**matched_var_exp**
 '   MAX_STRATS = 100'

   &ensp;**isEq**
 '   False'

### Item v1

   &ensp;**info**
 '  &emsp; 
- Description: Performance fee (defaults to 10%) 
   - Possible Var Names from ChatGPT: ['defaultPerformanceFee', 'performanceFeePercentage', 'basePerformanceFee'] 
   - Expression:  0.1 
'

   &ensp;**Is the fee found**
 '   No'

   &ensp;**matched_var_name**
 '   performanceFee'

   &ensp;**matched_var_exp**
 '   performanceFee = '

   &ensp;**isEq**
 '   False'

### Item v2

   &ensp;**info**
 '  &emsp; 
- Description: Management fee (defaults to 0%) 
   - Possible Var Names from ChatGPT: ['managementFee', 'defaultManagementFee', 'adminFeePercentage'] 
   - Expression:  0 
'

   &ensp;**Is the fee found**
 '   No'

   &ensp;**matched_var_name**
 '   managementFee'

   &ensp;**matched_var_exp**
 '   managementFee = '

   &ensp;**isEq**
 '   False'

### Item v3

   &ensp;**info**
 '  &emsp; 
- Description: To limit losses, our strategy automatically rebalances the portfolio if the price shifts around 8% in either direction, limiting our losses to about .08% for each interval. 
   - Possible Var Names from ChatGPT: ['rebalanceThreshold', 'maxPriceShiftPercent', 'lossLimitPerInterval'] 
   - Expression:  0.08 
'

   &ensp;**Is the fee found**
 '   No'

   &ensp;**matched_var_name**
 '   rebalanceThreshold'

   &ensp;**matched_var_exp**
 '   rebalanceThreshold = 400'

   &ensp;**isEq**
 '   False'


## hidden_fee_function


## hidden_fee_var

### INTEREST_RATE_MODE_VARIABLE

  &ensp;** Possible Values **:
 '2'

### LIQUIDATION_PROTOCOL_FEE_MASK

  &ensp;** Possible Values **:
 '0xFFFFFFFFFFFFFFFFFFFFFF0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'

### LIQUIDATION_PROTOCOL_FEE_START_BIT_POSITION

  &ensp;** Possible Values **:
 '152'

### MAX_VALID_LIQUIDATION_PROTOCOL_FEE

  &ensp;** Possible Values **:
 '65535'

### MAX_MANAGEMENT_FEE

  &ensp;** Possible Values **:
 '.05e18'

### MAX_PERFORMANCE_FEE

  &ensp;** Possible Values **:
 '.25e18'

### epochExchangeRate_epoch_

  &ensp;** Possible Values **:
 'exchangeRate'

### exchangeRate

  &ensp;** Possible Values **:
 'mulDivDown(1000000000000000000000000000000000000.0, 0)'


