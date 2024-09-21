## whitepaper

### Item v0

   &ensp;**info**
   &emsp; 
- Description: Max Supply: 150,000,000 
   - Possible Var Names from ChatGPT: ['maxSupply', 'totalMaxSupply', 'MAX_TOKEN_SUPPLY'] 
   - Expression:  150000000 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    MAX_SUPPLY

   &ensp;**matched_var_exp**
    MAX_SUPPLY = 150_000_000 * 10 ** 18

   &ensp;**isEq**
    True

### Item v1

   &ensp;**info**
   &emsp; 
- Description: Initial Total Supply: 10,000,000 Token 
   - Possible Var Names from ChatGPT: ['initialTotalSupply', 'startingTokenSupply', 'initialSupplyTokens'] 
   - Expression:  10000000 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    LIQUIDITY_AMOUNT

   &ensp;**matched_var_exp**
    LIQUIDITY_AMOUNT = 3_375_000 * 10 ** 18

   &ensp;**isEq**
    False

### Item v2

   &ensp;**info**
   &emsp; 
- Description: Initial Current Circulating Supply: 500,000 Tokens (Max) 
   - Possible Var Names from ChatGPT: ['initialMaxCirculatingSupply', 'maxStartingCirculation', 'initialCirculationCap'] 
   - Expression:  500000 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    MAX_SUPPLY

   &ensp;**matched_var_exp**
    MAX_SUPPLY = 150_000_000 * 10 ** 18

   &ensp;**isEq**
    False

### Item v3

   &ensp;**info**
   &emsp; 
- Description: Team token: The team tokens will only be minted after 1 year from the listing day and then locked for another year making the total vesting period 2 years. 
   - Possible Var Names from ChatGPT: ['teamTokenVestingDuration', 'teamTokensLockedPeriod', 'teamTokenMintLockPeriod'] 
   - Expression:  15000000 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    MAX_TEAM_SUPPLY

   &ensp;**matched_var_exp**
    MAX_TEAM_SUPPLY = 15_000_000 * 10 ** 18

   &ensp;**isEq**
    True

### Item v4

   &ensp;**info**
   &emsp; 
- Description: Community token: The community tokens will be minted through staking/farming rewards and referrals. 
   - Possible Var Names from ChatGPT: ['communityRewardToken', 'mintedCommunityToken', 'stakeReferralToken'] 
   - Expression:  105000000 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    MAX_COMMUNITY_SUPPLY

   &ensp;**matched_var_exp**
    MAX_COMMUNITY_SUPPLY = 105_000_000 * 10 ** 18

   &ensp;**isEq**
    True

### Item v5

   &ensp;**info**
   &emsp; 
- Description: Company reserve: The company reserve token will serve as the project development and marketing funds. The tokens will be locked for 6 months from the listing day and then will be subject to a Governance vote for usage. The total allocation will be minted over time. 
   - Possible Var Names from ChatGPT: ['companyReserveAllocation', 'projectDevelopmentFund', 'marketingReserveTokens'] 
   - Expression:  11250000 


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    COMPANY_RESERVE_AMOUNT

   &ensp;**matched_var_exp**
    COMPANY_RESERVE_AMOUNT = 11_250_000 * 10 ** 18

   &ensp;**isEq**
    True

### Item v6

   &ensp;**info**
   &emsp; 
- Description: Airdrop: The initial Launch Airdrop 
   - Possible Var Names from ChatGPT: ['initialAirdropAllocation', 'launchAirdropAmount', 'seedAirdropBalance'] 
   - Expression:  375000 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    AIRDROP_AMOUNT

   &ensp;**matched_var_exp**
    AIRDROP_AMOUNT = 250_000 * 10 ** 18

   &ensp;**isEq**
    False

### Item v7

   &ensp;**info**
   &emsp; 
- Description: ICO: The tokens reserved for the initial coin offering of GloryFinance. The unsold token from ICO will be burned. 1,000,000 tokens will be minted for the ICO as a start. The remaining tokens will be only minted if necessary. 
   - Possible Var Names from ChatGPT: ['icoReservedTokens', 'initialCoinsOffered', 'icoMintedTokens'] 
   - Expression:  15000000 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    teamMinted

   &ensp;**matched_var_exp**
    teamMinted = true

   &ensp;**isEq**
    False

### Item v8

   &ensp;**info**
   &emsp; 
- Description: Liquidity: The tokens are reserved for Liquidity injection. The total allocation will be minted over time. 
   - Possible Var Names from ChatGPT: ['liquidityAllocation', 'liquidityInjectionTokens', 'mintedLiquidityReserve'] 
   - Expression:  3375000  


   &ensp;**Is the fee found**
    Yes

   &ensp;**matched_var_name**
    LIQUIDITY_AMOUNT

   &ensp;**matched_var_exp**
    LIQUIDITY_AMOUNT = 3_375_000 * 10 ** 18

   &ensp;**isEq**
    True


## hidden_fee_function


## hidden_fee_var

### receiveFeeAddress

  &ensp;** Possible Values **:
 _receiveFeeAddress

### amountFee

  &ensp;** Possible Values **:
 amount - amountTransfer


