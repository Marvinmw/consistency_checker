## whitepaper

### Item v0

   &ensp;**info**
 '  &emsp; 
- Description: When a user's collateral value falls below the required 150%, (relative to their minted DYAD), they can be liquidated. Anyone can trigger a liquidation.  
   - Possible Var Names from ChatGPT: ['minimumCollateralPercentage', 'liquidationThreshold', 'collateralizationRatio'] 
   - Expression:  1.5 
'

   &ensp;**Is the fee found**
 '   No'

   &ensp;**matched_var_name**
 '   LIQUIDATION_REWARD'

   &ensp;**matched_var_exp**
 '   LIQUIDATION_REWARD = 0.2e18'

   &ensp;**isEq**
 '   False'

### Item v1

   &ensp;**info**
 '  &emsp; 
- Description: The liquidator repays the outstanding minted DYAD and receives collateral, plus a 20% bonus, in return. 
   - Possible Var Names from ChatGPT: ['liquidationBonusPercentage', 'collateralRedemptionBonus', 'repaymentBonusRatio'] 
   - Expression:  0.2 
'

   &ensp;**Is the fee found**
 '   Yes'

   &ensp;**matched_var_name**
 '   LIQUIDATION_REWARD'

   &ensp;**matched_var_exp**
 '   LIQUIDATION_REWARD = 0.2e18'

   &ensp;**isEq**
 '   True'

### Item v2

   &ensp;**info**
 '  &emsp; 
- Description: The total supply of the Kerosene token is one Billion.  
   - Possible Var Names from ChatGPT: ['totalKeroseneSupply', 'keroseneTokenSupply', 'maxKeroseneTokens'] 
   - Expression:  1000000000 
'

   &ensp;**Is the fee found**
 '   No'

   &ensp;**matched_var_name**
 '   totalKeroseneInVault'

   &ensp;**matched_var_exp**
 '   totalKeroseneInVault = '

   &ensp;**isEq**
 '   Eq(_rewardToken, 2.0e+17)'


## hidden_fee_function


## hidden_fee_var

### GOERLI_FEE

  &ensp;** Possible Values **:
 '0.001e18'

### GOERLI_FEE_RECIPIENT

  &ensp;** Possible Values **:
 '0xDeD796De6a14E255487191963dEe436c45995813'

### MAINNET_FEE

  &ensp;** Possible Values **:
 '0.0015e18'

### MAINNET_FEE_RECIPIENT

  &ensp;** Possible Values **:
 '0xDeD796De6a14E255487191963dEe436c45995813'

### SEPOLIA_FEE

  &ensp;** Possible Values **:
 '0.001e18'

### SEPOLIA_FEE_RECIPIENT

  &ensp;** Possible Values **:
 '0xDeD796De6a14E255487191963dEe436c45995813'


