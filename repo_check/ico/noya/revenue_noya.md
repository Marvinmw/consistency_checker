## whitepaper

### Item v0

   &ensp;**info**
 '  &emsp; 
- Description: Withdrawal fee: It's a percentage of user's withdrawal (currently is 0%). It occurs in the 'executeWithdraw' function of the accountingManager contract. 
   - Possible Var Names from ChatGPT: ['withdrawalFeePercentage', 'executeWithdrawFee', 'accountingManagerWithdrawalFee'] 
   - Expression:  0 
'

   &ensp;**Is the fee found**
 '   Yes'

   &ensp;**matched_var_name**
 '   amountAskedForWithdraw'

   &ensp;**matched_var_exp**
 '   amountAskedForWithdraw = 0'

   &ensp;**isEq**
 '   True'

### Item v1

   &ensp;**info**
 '  &emsp; 
- Description: Management fee: The manager simply mint x% of the total shares * (time_elapsed_from_last_fee / seconds_in_year) to the feeReceiver periodically (at most every 10 days). The manager will call the 'collectManagementFees' function of the accountingManager contract to redeem this fee. 
   - Possible Var Names from ChatGPT: ['managementFeeRate', 'periodicMintedFee', 'accumulatedManagementFee'] 
   - Expression:  0 
'

   &ensp;**Is the fee found**
 '   Yes'

   &ensp;**matched_var_name**
 '   managementFee'

   &ensp;**matched_var_exp**
 '   managementFee = '

   &ensp;**isEq**
 '   True'

### Item v2

   &ensp;**info**
 '  &emsp; 
- Description: Performance fee:If the noya vault makes any profit, the strategy manager will get a percentage of that profit. To ensure that this is actually the profit and the manager is not manipulating the vault, there is a 2 step process to get this fee. 1. First the strategy manager calls the “recordProfitForFee “ function to calculate the shares of the fees and store the fee amount in “preformanceFeeSharesWaitingForDistribution “ variable. 2. It has to wait for at least 12 hours. During this 12 hours, if the profit of noya goes lower than the profit amount at the end of step 1, anyone can call the function 'checkIfTVLHasDroped' and the fees that were recorded in the step 1 will be put to 0. To get the fees again, the manager has to do the first step again and wait for 12 hours. If the profit doesn’t drop within 12 hours, it means that there was no manipulation. Then it can call 'collectPerformanceFees' function of the accountingManager and get the performance fee. 
   - Possible Var Names from ChatGPT: ['pendingPerformanceFee', 'accumulatedFeeReserve', 'managerProfitShare'] 
   - Expression:  0 
'

   &ensp;**Is the fee found**
 '   No'

   &ensp;**matched_var_name**
 '   performanceFee'

   &ensp;**matched_var_exp**
 '   performanceFee = '

   &ensp;**isEq**
 '   Eq(getProfit(), 0)'


## hidden_fee_function

### collectManagementFees

  &ensp;** Possible Values **:
 '(0, 0), 
 (2.73972602739726e-8*managementFee*(-currentFeeShares + totalShares), 10)'


## hidden_fee_var

### FEE_PRECISION

  &ensp;** Possible Values **:
 '1e6'

### WITHDRAWAL_MAX_FEE

  &ensp;** Possible Values **:
 '5e4'

### MANAGEMENT_MAX_FEE

  &ensp;** Possible Values **:
 '5e5'

### PERFORMANCE_MAX_FEE

  &ensp;** Possible Values **:
 '1e5'

### withdrawFeeReceiver

  &ensp;** Possible Values **:
 '_withdrawFeeReceiver'

### performanceFeeReceiver

  &ensp;** Possible Values **:
 '_performanceFeeReceiver'

### managementFeeReceiver

  &ensp;** Possible Values **:
 '_managementFeeReceiver'

### withdrawFee

  &ensp;** Possible Values **:
 '_withdrawFee'

### performanceFee

  &ensp;** Possible Values **:
 '_performanceFee'

### withdrawFeeAmount

  &ensp;** Possible Values **:
 '0'

### feeAmount

  &ensp;** Possible Values **:
 '1.0e-6*baseTokenAmount*withdrawFee'

### storedProfitForFee

  &ensp;** Possible Values **:
 '0, 
 -totalAWFDeposit - totalDepositedAmount + totalWithdrawnAmount + balanceOf(address(this)) + getTVL(0, registry, address(baseToken))'

### preformanceFeeSharesWaitingForDistribution

  &ensp;** Possible Values **:
 'previewDeposit(1.0e-6*performanceFee*(storedProfitForFee - totalProfitCalculated)), 
 0, 
 0'

### lastFeeDistributionTime

  &ensp;** Possible Values **:
 'timestamp'

### currentFeeShares

  &ensp;** Possible Values **:
 'preformanceFeeSharesWaitingForDistribution + balanceOf(managementFeeReceiver) + balanceOf(performanceFeeReceiver)'

### managementFeeAmount

  &ensp;** Possible Values **:
 '2.73972602739726e-8*managementFee*(-currentFeeShares + totalShares)'


