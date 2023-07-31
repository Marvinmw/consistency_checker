Summary
 - [arbitrary-send-eth](#arbitrary-send-eth) (2 results) (High)
 - [reentrancy-eth](#reentrancy-eth) (4 results) (High)
 - [unchecked-lowlevel](#unchecked-lowlevel) (1 results) (Medium)
 - [unused-return](#unused-return) (1 results) (Medium)
 - [events-maths](#events-maths) (8 results) (Low)
 - [missing-zero-check](#missing-zero-check) (4 results) (Low)
 - [calls-loop](#calls-loop) (1 results) (Low)
 - [reentrancy-benign](#reentrancy-benign) (4 results) (Low)
 - [reentrancy-events](#reentrancy-events) (4 results) (Low)
 - [timestamp](#timestamp) (4 results) (Low)
 - [boolean-equal](#boolean-equal) (1 results) (Informational)
 - [costly-loop](#costly-loop) (3 results) (Informational)
 - [dead-code](#dead-code) (9 results) (Informational)
 - [function-init-state](#function-init-state) (2 results) (Informational)
 - [solc-version](#solc-version) (8 results) (Informational)
 - [low-level-calls](#low-level-calls) (3 results) (Informational)
 - [naming-convention](#naming-convention) (32 results) (Informational)
 - [similar-names](#similar-names) (1 results) (Informational)
 - [too-many-digits](#too-many-digits) (1 results) (Informational)
 - [unused-state](#unused-state) (1 results) (Informational)
 - [constable-states](#constable-states) (5 results) (Optimization)
## arbitrary-send-eth
Impact: High
Confidence: Medium
 - [ ] ID-0
[MoonGame.swapBack()](contracts/MoonGame.sol#L218-L258) sends eth to arbitrary user
	Dangerous calls:
	- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)
	- [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)

contracts/MoonGame.sol#L218-L258


 - [ ] ID-1
[MoonGame.buyTokens(uint256,address)](contracts/MoonGame.sol#L287-L298) sends eth to arbitrary user
	Dangerous calls:
	- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)

contracts/MoonGame.sol#L287-L298


## reentrancy-eth
Impact: High
Confidence: Medium
 - [ ] ID-2
Reentrancy in [DividendDistributor.setShare(address,uint256)](contracts/DividendDistributor.sol#L55-L69):
	External calls:
	- [distributeDividend(shareholder)](contracts/DividendDistributor.sol#L57)
		- [(success) = address(shareholder).call{value: amount}()](contracts/DividendDistributor.sol#L114)
	State variables written after the call(s):
	- [shares[shareholder].amount = amount](contracts/DividendDistributor.sol#L67)
	- [shares[shareholder].totalExcluded = getCumulativeDividends(shares[shareholder].amount)](contracts/DividendDistributor.sol#L68)

contracts/DividendDistributor.sol#L55-L69


 - [ ] ID-3
Reentrancy in [MoonGame._transferFrom(address,address,uint256)](contracts/MoonGame.sol#L145-L166):
	External calls:
	- [swapBack()](contracts/MoonGame.sol#L149)
		- [router.swapExactTokensForETHSupportingFeeOnTransferTokens(amountToSwap,0,path,address(this),block.timestamp)](contracts/MoonGame.sol#L228-L234)
		- [distributor.deposit{value: amountBNBReflection}()](contracts/MoonGame.sol#L244)
		- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)
		- [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)
	- [triggerAutoBuyback()](contracts/MoonGame.sol#L150)
		- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)
	External calls sending eth:
	- [swapBack()](contracts/MoonGame.sol#L149)
		- [distributor.deposit{value: amountBNBReflection}()](contracts/MoonGame.sol#L244)
		- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)
		- [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)
	- [triggerAutoBuyback()](contracts/MoonGame.sol#L150)
		- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)
	State variables written after the call(s):
	- [_balances[sender] = _balances[sender].sub(amount,Insufficient Balance)](contracts/MoonGame.sol#L154)
	- [_balances[recipient] = _balances[recipient].add(amountReceived)](contracts/MoonGame.sol#L157)
	- [amountReceived = takeFee(sender,recipient,amount)](contracts/MoonGame.sol#L156)
		- [_balances[address(this)] = _balances[address(this)].add(feeAmount)](contracts/MoonGame.sol#L205)
	- [triggerAutoBuyback()](contracts/MoonGame.sol#L150)
		- [inSwap = true](contracts/MoonGame.sol#L78)
		- [inSwap = false](contracts/MoonGame.sol#L78)

contracts/MoonGame.sol#L145-L166


 - [ ] ID-4
Reentrancy in [DividendDistributor.process(uint256)](contracts/DividendDistributor.sol#L77-L101):
	External calls:
	- [distributeDividend(shareholders[currentIndex])](contracts/DividendDistributor.sol#L93)
		- [(success) = address(shareholder).call{value: amount}()](contracts/DividendDistributor.sol#L114)
	State variables written after the call(s):
	- [currentIndex ++](contracts/DividendDistributor.sol#L98)

contracts/DividendDistributor.sol#L77-L101


 - [ ] ID-5
Reentrancy in [DividendDistributor.distributeDividend(address)](contracts/DividendDistributor.sol#L108-L121):
	External calls:
	- [(success) = address(shareholder).call{value: amount}()](contracts/DividendDistributor.sol#L114)
	State variables written after the call(s):
	- [shares[shareholder].totalRealised = shares[shareholder].totalRealised.add(amount)](contracts/DividendDistributor.sol#L117)
	- [shares[shareholder].totalExcluded = getCumulativeDividends(shares[shareholder].amount)](contracts/DividendDistributor.sol#L118)

contracts/DividendDistributor.sol#L108-L121


## unchecked-lowlevel
Impact: Medium
Confidence: Medium
 - [ ] ID-6
[MoonGame.swapBack()](contracts/MoonGame.sol#L218-L258) ignores return value by [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)

contracts/MoonGame.sol#L218-L258


## unused-return
Impact: Medium
Confidence: Medium
 - [ ] ID-7
[MoonGame.swapBack()](contracts/MoonGame.sol#L218-L258) ignores return value by [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)

contracts/MoonGame.sol#L218-L258


## events-maths
Impact: Low
Confidence: Medium
 - [ ] ID-8
[DividendDistributor.deposit()](contracts/DividendDistributor.sol#L71-L75) should emit an event for: 
	- [dividendsPerShare = dividendsPerShare.add(dividendsPerShareAccuracyFactor.mul(amount).div(totalShares))](contracts/DividendDistributor.sol#L74) 

contracts/DividendDistributor.sol#L71-L75


 - [ ] ID-9
[MoonGame.setTxLimit(uint256)](contracts/MoonGame.sol#L326-L329) should emit an event for: 
	- [_maxTxAmount = amount](contracts/MoonGame.sol#L328) 

contracts/MoonGame.sol#L326-L329


 - [ ] ID-10
[MoonGame.setAutoBuybackSettings(bool,uint256,uint256,uint256)](contracts/MoonGame.sol#L300-L307) should emit an event for: 
	- [autoBuybackCap = _cap](contracts/MoonGame.sol#L302) 
	- [autoBuybackAmount = _amount](contracts/MoonGame.sol#L304) 

contracts/MoonGame.sol#L300-L307


 - [ ] ID-11
[MoonGame.setBuybackMultiplierSettings(uint256,uint256,uint256)](contracts/MoonGame.sol#L309-L314) should emit an event for: 
	- [buybackMultiplierNumerator = numerator](contracts/MoonGame.sol#L311) 
	- [buybackMultiplierDenominator = denominator](contracts/MoonGame.sol#L312) 
	- [buybackMultiplierLength = length](contracts/MoonGame.sol#L313) 

contracts/MoonGame.sol#L309-L314


 - [ ] ID-12
[MoonGame.setFees(uint256,uint256,uint256,uint256,uint256)](contracts/MoonGame.sol#L349-L357) should emit an event for: 
	- [liquidityFee = _liquidityFee](contracts/MoonGame.sol#L350) 
	- [reflectionFee = _reflectionFee](contracts/MoonGame.sol#L352) 
	- [marketingFee = _marketingFee](contracts/MoonGame.sol#L353) 
	- [totalFee = _liquidityFee.add(_buybackFee).add(_reflectionFee).add(_marketingFee)](contracts/MoonGame.sol#L354) 
	- [feeDenominator = _feeDenominator](contracts/MoonGame.sol#L355) 

contracts/MoonGame.sol#L349-L357


 - [ ] ID-13
[DividendDistributor.setDistributionCriteria(uint256,uint256)](contracts/DividendDistributor.sol#L50-L53) should emit an event for: 
	- [minPeriod = _minPeriod](contracts/DividendDistributor.sol#L51) 
	- [minDistribution = _minDistribution](contracts/DividendDistributor.sol#L52) 

contracts/DividendDistributor.sol#L50-L53


 - [ ] ID-14
[MoonGame.setSwapBackSettings(bool,uint256)](contracts/MoonGame.sol#L364-L367) should emit an event for: 
	- [swapThreshold = _amount](contracts/MoonGame.sol#L366) 

contracts/MoonGame.sol#L364-L367


 - [ ] ID-15
[MoonGame.setTargetLiquidity(uint256,uint256)](contracts/MoonGame.sol#L369-L372) should emit an event for: 
	- [targetLiquidity = _target](contracts/MoonGame.sol#L370) 
	- [targetLiquidityDenominator = _denominator](contracts/MoonGame.sol#L371) 

contracts/MoonGame.sol#L369-L372


## missing-zero-check
Impact: Low
Confidence: Medium
 - [ ] ID-16
[MoonGame.setFeeReceivers(address,address)._autoLiquidityReceiver](contracts/MoonGame.sol#L359) lacks a zero-check on :
		- [autoLiquidityReceiver = _autoLiquidityReceiver](contracts/MoonGame.sol#L360)

contracts/MoonGame.sol#L359


 - [ ] ID-17
[MoonGame.withDrawBNB(address,uint256).to](contracts/MoonGame.sol#L395) lacks a zero-check on :
		- [(success) = address(to).call{value: amount}()](contracts/MoonGame.sol#L397)

contracts/MoonGame.sol#L395


 - [ ] ID-18
[MoonGame.setFeeReceivers(address,address)._marketingFeeReceiver](contracts/MoonGame.sol#L359) lacks a zero-check on :
		- [marketingFeeReceiver = _marketingFeeReceiver](contracts/MoonGame.sol#L361)

contracts/MoonGame.sol#L359


 - [ ] ID-19
[Auth.transferOwnership(address).adr](contracts/Auth.sol#L60) lacks a zero-check on :
		- [owner = adr](contracts/Auth.sol#L61)

contracts/Auth.sol#L60


## calls-loop
Impact: Low
Confidence: Medium
 - [ ] ID-20
[DividendDistributor.distributeDividend(address)](contracts/DividendDistributor.sol#L108-L121) has external calls inside a loop: [(success) = address(shareholder).call{value: amount}()](contracts/DividendDistributor.sol#L114)

contracts/DividendDistributor.sol#L108-L121


## reentrancy-benign
Impact: Low
Confidence: Medium
 - [ ] ID-21
Reentrancy in [MoonGame.triggerAutoBuyback()](contracts/MoonGame.sol#L280-L285):
	External calls:
	- [buyTokens(autoBuybackAmount,DEAD)](contracts/MoonGame.sol#L281)
		- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)
	State variables written after the call(s):
	- [autoBuybackAccumulator = autoBuybackAccumulator.add(autoBuybackAmount)](contracts/MoonGame.sol#L283)
	- [autoBuybackBlockLast = block.number](contracts/MoonGame.sol#L282)
	- [autoBuybackEnabled = false](contracts/MoonGame.sol#L284)

contracts/MoonGame.sol#L280-L285


 - [ ] ID-22
Reentrancy in [DividendDistributor.setShare(address,uint256)](contracts/DividendDistributor.sol#L55-L69):
	External calls:
	- [distributeDividend(shareholder)](contracts/DividendDistributor.sol#L57)
		- [(success) = address(shareholder).call{value: amount}()](contracts/DividendDistributor.sol#L114)
	State variables written after the call(s):
	- [addShareholder(shareholder)](contracts/DividendDistributor.sol#L61)
		- [shareholderIndexes[shareholder] = shareholders.length](contracts/DividendDistributor.sol#L143)
	- [removeShareholder(shareholder)](contracts/DividendDistributor.sol#L63)
		- [shareholderIndexes[shareholders[shareholders.length - 1]] = shareholderIndexes[shareholder]](contracts/DividendDistributor.sol#L149)
	- [addShareholder(shareholder)](contracts/DividendDistributor.sol#L61)
		- [shareholders.push(shareholder)](contracts/DividendDistributor.sol#L144)
	- [removeShareholder(shareholder)](contracts/DividendDistributor.sol#L63)
		- [shareholders[shareholderIndexes[shareholder]] = shareholders[shareholders.length - 1]](contracts/DividendDistributor.sol#L148)
		- [shareholders.pop()](contracts/DividendDistributor.sol#L150)
	- [totalShares = totalShares.sub(shares[shareholder].amount).add(amount)](contracts/DividendDistributor.sol#L66)

contracts/DividendDistributor.sol#L55-L69


 - [ ] ID-23
Reentrancy in [MoonGame.triggerZeusBuyback(uint256,bool)](contracts/MoonGame.sol#L268-L274):
	External calls:
	- [buyTokens(amount,DEAD)](contracts/MoonGame.sol#L269)
		- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)
	State variables written after the call(s):
	- [buybackMultiplierTriggeredAt = block.timestamp](contracts/MoonGame.sol#L271)

contracts/MoonGame.sol#L268-L274


 - [ ] ID-24
Reentrancy in [DividendDistributor.distributeDividend(address)](contracts/DividendDistributor.sol#L108-L121):
	External calls:
	- [(success) = address(shareholder).call{value: amount}()](contracts/DividendDistributor.sol#L114)
	State variables written after the call(s):
	- [shareholderClaims[shareholder] = block.timestamp](contracts/DividendDistributor.sol#L116)

contracts/DividendDistributor.sol#L108-L121


## reentrancy-events
Impact: Low
Confidence: Medium
 - [ ] ID-25
Reentrancy in [MoonGame._transferFrom(address,address,uint256)](contracts/MoonGame.sol#L145-L166):
	External calls:
	- [swapBack()](contracts/MoonGame.sol#L149)
		- [router.swapExactTokensForETHSupportingFeeOnTransferTokens(amountToSwap,0,path,address(this),block.timestamp)](contracts/MoonGame.sol#L228-L234)
		- [distributor.deposit{value: amountBNBReflection}()](contracts/MoonGame.sol#L244)
		- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)
		- [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)
	- [triggerAutoBuyback()](contracts/MoonGame.sol#L150)
		- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)
	External calls sending eth:
	- [swapBack()](contracts/MoonGame.sol#L149)
		- [distributor.deposit{value: amountBNBReflection}()](contracts/MoonGame.sol#L244)
		- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)
		- [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)
	- [triggerAutoBuyback()](contracts/MoonGame.sol#L150)
		- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)
	Event emitted after the call(s):
	- [Transfer(sender,address(this),feeAmount)](contracts/MoonGame.sol#L206)
		- [amountReceived = takeFee(sender,recipient,amount)](contracts/MoonGame.sol#L156)

contracts/MoonGame.sol#L145-L166


 - [ ] ID-26
Reentrancy in [MoonGame._transferFrom(address,address,uint256)](contracts/MoonGame.sol#L145-L166):
	External calls:
	- [swapBack()](contracts/MoonGame.sol#L149)
		- [router.swapExactTokensForETHSupportingFeeOnTransferTokens(amountToSwap,0,path,address(this),block.timestamp)](contracts/MoonGame.sol#L228-L234)
		- [distributor.deposit{value: amountBNBReflection}()](contracts/MoonGame.sol#L244)
		- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)
		- [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)
	- [triggerAutoBuyback()](contracts/MoonGame.sol#L150)
		- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)
	- [distributor.setShare(sender,_balances[sender])](contracts/MoonGame.sol#L159)
	- [distributor.setShare(recipient,_balances[recipient])](contracts/MoonGame.sol#L160)
	- [distributor.process(distributorGas)](contracts/MoonGame.sol#L162)
	External calls sending eth:
	- [swapBack()](contracts/MoonGame.sol#L149)
		- [distributor.deposit{value: amountBNBReflection}()](contracts/MoonGame.sol#L244)
		- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)
		- [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)
	- [triggerAutoBuyback()](contracts/MoonGame.sol#L150)
		- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)
	Event emitted after the call(s):
	- [Transfer(sender,recipient,amountReceived)](contracts/MoonGame.sol#L164)

contracts/MoonGame.sol#L145-L166


 - [ ] ID-27
Reentrancy in [MoonGame.swapBack()](contracts/MoonGame.sol#L218-L258):
	External calls:
	- [router.swapExactTokensForETHSupportingFeeOnTransferTokens(amountToSwap,0,path,address(this),block.timestamp)](contracts/MoonGame.sol#L228-L234)
	- [distributor.deposit{value: amountBNBReflection}()](contracts/MoonGame.sol#L244)
	- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)
	- [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)
	External calls sending eth:
	- [distributor.deposit{value: amountBNBReflection}()](contracts/MoonGame.sol#L244)
	- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)
	- [router.addLiquidityETH{value: amountBNBLiquidity}(address(this),amountToLiquify,0,0,autoLiquidityReceiver,block.timestamp)](contracts/MoonGame.sol#L248-L255)
	Event emitted after the call(s):
	- [AutoLiquify(amountBNBLiquidity,amountToLiquify)](contracts/MoonGame.sol#L256)

contracts/MoonGame.sol#L218-L258


 - [ ] ID-28
Reentrancy in [MoonGame.triggerZeusBuyback(uint256,bool)](contracts/MoonGame.sol#L268-L274):
	External calls:
	- [buyTokens(amount,DEAD)](contracts/MoonGame.sol#L269)
		- [router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(0,path,to,block.timestamp)](contracts/MoonGame.sol#L292-L297)
	Event emitted after the call(s):
	- [BuybackMultiplierActive(buybackMultiplierLength)](contracts/MoonGame.sol#L272)

contracts/MoonGame.sol#L268-L274


## timestamp
Impact: Low
Confidence: Medium
 - [ ] ID-29
[DividendDistributor.shouldDistribute(address)](contracts/DividendDistributor.sol#L103-L106) uses timestamp for comparisons
	Dangerous comparisons:
	- [shareholderClaims[shareholder] + minPeriod < block.timestamp && getUnpaidEarnings(shareholder) > minDistribution](contracts/DividendDistributor.sol#L104-L105)

contracts/DividendDistributor.sol#L103-L106


 - [ ] ID-30
[MoonGame.isOverLiquified(uint256,uint256)](contracts/MoonGame.sol#L391-L393) uses timestamp for comparisons
	Dangerous comparisons:
	- [getLiquidityBacking(accuracy) > target](contracts/MoonGame.sol#L392)

contracts/MoonGame.sol#L391-L393


 - [ ] ID-31
[MoonGame.getMultipliedFee()](contracts/MoonGame.sol#L191-L200) uses timestamp for comparisons
	Dangerous comparisons:
	- [launchedAtTimestamp + 86400 > block.timestamp](contracts/MoonGame.sol#L192)
	- [buybackMultiplierTriggeredAt.add(buybackMultiplierLength) > block.timestamp](contracts/MoonGame.sol#L194)

contracts/MoonGame.sol#L191-L200


 - [ ] ID-32
[MoonGame.shouldSwapBack()](contracts/MoonGame.sol#L211-L216) uses timestamp for comparisons
	Dangerous comparisons:
	- [msg.sender != pair && ! inSwap && swapEnabled && _balances[address(this)] >= swapThreshold](contracts/MoonGame.sol#L212-L215)

contracts/MoonGame.sol#L211-L216


## boolean-equal
Impact: Informational
Confidence: High
 - [ ] ID-33
[MoonGame.onlyBuybacker()](contracts/MoonGame.sol#L114) compares to a boolean constant:
	-[require(bool,string)(buyBacker[msg.sender] == true,)](contracts/MoonGame.sol#L114)

contracts/MoonGame.sol#L114


## costly-loop
Impact: Informational
Confidence: Medium
 - [ ] ID-34
[DividendDistributor.process(uint256)](contracts/DividendDistributor.sol#L77-L101) has costly operations inside a loop:
	- [currentIndex ++](contracts/DividendDistributor.sol#L98)

contracts/DividendDistributor.sol#L77-L101


 - [ ] ID-35
[DividendDistributor.process(uint256)](contracts/DividendDistributor.sol#L77-L101) has costly operations inside a loop:
	- [currentIndex = 0](contracts/DividendDistributor.sol#L89)

contracts/DividendDistributor.sol#L77-L101


 - [ ] ID-36
[DividendDistributor.distributeDividend(address)](contracts/DividendDistributor.sol#L108-L121) has costly operations inside a loop:
	- [totalDistributed = totalDistributed.add(amount)](contracts/DividendDistributor.sol#L113)

contracts/DividendDistributor.sol#L108-L121


## dead-code
Impact: Informational
Confidence: Medium
 - [ ] ID-37
[SafeMath.tryDiv(uint256,uint256)](contracts/SafeMath.sol#L63-L68) is never used and should be removed

contracts/SafeMath.sol#L63-L68


 - [ ] ID-38
[SafeMath.tryMod(uint256,uint256)](contracts/SafeMath.sol#L75-L80) is never used and should be removed

contracts/SafeMath.sol#L75-L80


 - [ ] ID-39
[SafeMath.tryAdd(uint256,uint256)](contracts/SafeMath.sol#L21-L27) is never used and should be removed

contracts/SafeMath.sol#L21-L27


 - [ ] ID-40
[SafeMath.mod(uint256,uint256,string)](contracts/SafeMath.sol#L212-L217) is never used and should be removed

contracts/SafeMath.sol#L212-L217


 - [ ] ID-41
[SafeMath.div(uint256,uint256,string)](contracts/SafeMath.sol#L190-L195) is never used and should be removed

contracts/SafeMath.sol#L190-L195


 - [ ] ID-42
[SafeMath.mod(uint256,uint256)](contracts/SafeMath.sol#L150-L152) is never used and should be removed

contracts/SafeMath.sol#L150-L152


 - [ ] ID-43
[SafeMath.tryMul(uint256,uint256)](contracts/SafeMath.sol#L46-L56) is never used and should be removed

contracts/SafeMath.sol#L46-L56


 - [ ] ID-44
[SafeMath.trySub(uint256,uint256)](contracts/SafeMath.sol#L34-L39) is never used and should be removed

contracts/SafeMath.sol#L34-L39


 - [ ] ID-45
[MoonGame.launched()](contracts/MoonGame.sol#L316-L318) is never used and should be removed

contracts/MoonGame.sol#L316-L318


## function-init-state
Impact: Informational
Confidence: High
 - [ ] ID-46
[MoonGame._maxTxAmount](contracts/MoonGame.sol#L28) is set pre-construction with a non-constant function or state variable:
	- _totalSupply.div(200)

contracts/MoonGame.sol#L28


 - [ ] ID-47
[MoonGame.swapThreshold](contracts/MoonGame.sol#L76) is set pre-construction with a non-constant function or state variable:
	- _totalSupply / 1000

contracts/MoonGame.sol#L76


## solc-version
Impact: Informational
Confidence: High
 - [ ] ID-48
Pragma version[^0.8.0](contracts/MoonGame.sol#L2) allows old versions

contracts/MoonGame.sol#L2


 - [ ] ID-49
solc-0.8.18 is not recommended for deployment

 - [ ] ID-50
Pragma version[^0.8.0](contracts/Auth.sol#L5) allows old versions

contracts/Auth.sol#L5


 - [ ] ID-51
Pragma version[^0.8.0](contracts/IDEXRouter.sol#L2) allows old versions

contracts/IDEXRouter.sol#L2


 - [ ] ID-52
Pragma version[^0.8.0](contracts/IBEP20.sol#L5) allows old versions

contracts/IBEP20.sol#L5


 - [ ] ID-53
Pragma version[^0.8.0](contracts/IDividendDistributor.sol#L2) allows old versions

contracts/IDividendDistributor.sol#L2


 - [ ] ID-54
Pragma version[^0.8.0](contracts/SafeMath.sol#L3) allows old versions

contracts/SafeMath.sol#L3


 - [ ] ID-55
Pragma version[^0.8.0](contracts/DividendDistributor.sol#L2) allows old versions

contracts/DividendDistributor.sol#L2


## low-level-calls
Impact: Informational
Confidence: High
 - [ ] ID-56
Low level call in [MoonGame.withDrawBNB(address,uint256)](contracts/MoonGame.sol#L395-L399):
	- [(success) = address(to).call{value: amount}()](contracts/MoonGame.sol#L397)

contracts/MoonGame.sol#L395-L399


 - [ ] ID-57
Low level call in [DividendDistributor.distributeDividend(address)](contracts/DividendDistributor.sol#L108-L121):
	- [(success) = address(shareholder).call{value: amount}()](contracts/DividendDistributor.sol#L114)

contracts/DividendDistributor.sol#L108-L121


 - [ ] ID-58
Low level call in [MoonGame.swapBack()](contracts/MoonGame.sol#L218-L258):
	- [address(marketingFeeReceiver).call{gas: 30000,value: amountBNBMarketing}()](contracts/MoonGame.sol#L245)

contracts/MoonGame.sol#L218-L258


## naming-convention
Impact: Informational
Confidence: High
 - [ ] ID-59
Parameter [MoonGame.setFeeReceivers(address,address)._autoLiquidityReceiver](contracts/MoonGame.sol#L359) is not in mixedCase

contracts/MoonGame.sol#L359


 - [ ] ID-60
Parameter [MoonGame.setFees(uint256,uint256,uint256,uint256,uint256)._reflectionFee](contracts/MoonGame.sol#L349) is not in mixedCase

contracts/MoonGame.sol#L349


 - [ ] ID-61
Function [IDEXRouter.WETH()](contracts/IDEXRouter.sol#L5) is not in mixedCase

contracts/IDEXRouter.sol#L5


 - [ ] ID-62
Parameter [MoonGame.setDistributionCriteria(uint256,uint256)._minDistribution](contracts/MoonGame.sol#L374) is not in mixedCase

contracts/MoonGame.sol#L374


 - [ ] ID-63
Parameter [MoonGame.setTargetLiquidity(uint256,uint256)._denominator](contracts/MoonGame.sol#L369) is not in mixedCase

contracts/MoonGame.sol#L369


 - [ ] ID-64
Variable [MoonGame.DEAD_NON_CHECKSUM](contracts/MoonGame.sol#L21) is not in mixedCase

contracts/MoonGame.sol#L21


 - [ ] ID-65
Variable [MoonGame._balances](contracts/MoonGame.sol#L30) is not in mixedCase

contracts/MoonGame.sol#L30


 - [ ] ID-66
Parameter [MoonGame.setAutoBuybackSettings(bool,uint256,uint256,uint256)._enabled](contracts/MoonGame.sol#L300) is not in mixedCase

contracts/MoonGame.sol#L300


 - [ ] ID-67
Parameter [MoonGame.setFees(uint256,uint256,uint256,uint256,uint256)._liquidityFee](contracts/MoonGame.sol#L349) is not in mixedCase

contracts/MoonGame.sol#L349


 - [ ] ID-68
Variable [MoonGame.DEAD](contracts/MoonGame.sol#L19) is not in mixedCase

contracts/MoonGame.sol#L19


 - [ ] ID-69
Variable [MoonGame.WBNB](contracts/MoonGame.sol#L18) is not in mixedCase

contracts/MoonGame.sol#L18


 - [ ] ID-70
Constant [MoonGame._symbol](contracts/MoonGame.sol#L24) is not in UPPER_CASE_WITH_UNDERSCORES

contracts/MoonGame.sol#L24


 - [ ] ID-71
Parameter [MoonGame.setSwapBackSettings(bool,uint256)._enabled](contracts/MoonGame.sol#L364) is not in mixedCase

contracts/MoonGame.sol#L364


 - [ ] ID-72
Parameter [MoonGame.setSwapBackSettings(bool,uint256)._amount](contracts/MoonGame.sol#L364) is not in mixedCase

contracts/MoonGame.sol#L364


 - [ ] ID-73
Parameter [MoonGame.setAutoBuybackSettings(bool,uint256,uint256,uint256)._cap](contracts/MoonGame.sol#L300) is not in mixedCase

contracts/MoonGame.sol#L300


 - [ ] ID-74
Parameter [MoonGame.setFees(uint256,uint256,uint256,uint256,uint256)._feeDenominator](contracts/MoonGame.sol#L349) is not in mixedCase

contracts/MoonGame.sol#L349


 - [ ] ID-75
Constant [MoonGame._name](contracts/MoonGame.sol#L23) is not in UPPER_CASE_WITH_UNDERSCORES

contracts/MoonGame.sol#L23


 - [ ] ID-76
Parameter [MoonGame.setAutoBuybackSettings(bool,uint256,uint256,uint256)._period](contracts/MoonGame.sol#L300) is not in mixedCase

contracts/MoonGame.sol#L300


 - [ ] ID-77
Parameter [DividendDistributor.setDistributionCriteria(uint256,uint256)._minDistribution](contracts/DividendDistributor.sol#L50) is not in mixedCase

contracts/DividendDistributor.sol#L50


 - [ ] ID-78
Constant [MoonGame._decimals](contracts/MoonGame.sol#L25) is not in UPPER_CASE_WITH_UNDERSCORES

contracts/MoonGame.sol#L25


 - [ ] ID-79
Parameter [DividendDistributor.setDistributionCriteria(uint256,uint256)._minPeriod](contracts/DividendDistributor.sol#L50) is not in mixedCase

contracts/DividendDistributor.sol#L50


 - [ ] ID-80
Variable [MoonGame._allowances](contracts/MoonGame.sol#L31) is not in mixedCase

contracts/MoonGame.sol#L31


 - [ ] ID-81
Variable [DividendDistributor._token](contracts/DividendDistributor.sol#L10) is not in mixedCase

contracts/DividendDistributor.sol#L10


 - [ ] ID-82
Parameter [MoonGame.setFeeReceivers(address,address)._marketingFeeReceiver](contracts/MoonGame.sol#L359) is not in mixedCase

contracts/MoonGame.sol#L359


 - [ ] ID-83
Parameter [MoonGame.setFees(uint256,uint256,uint256,uint256,uint256)._marketingFee](contracts/MoonGame.sol#L349) is not in mixedCase

contracts/MoonGame.sol#L349


 - [ ] ID-84
Parameter [MoonGame.setTargetLiquidity(uint256,uint256)._target](contracts/MoonGame.sol#L369) is not in mixedCase

contracts/MoonGame.sol#L369


 - [ ] ID-85
Parameter [MoonGame.setFees(uint256,uint256,uint256,uint256,uint256)._buybackFee](contracts/MoonGame.sol#L349) is not in mixedCase

contracts/MoonGame.sol#L349


 - [ ] ID-86
Variable [MoonGame.ZERO](contracts/MoonGame.sol#L20) is not in mixedCase

contracts/MoonGame.sol#L20


 - [ ] ID-87
Variable [MoonGame._maxTxAmount](contracts/MoonGame.sol#L28) is not in mixedCase

contracts/MoonGame.sol#L28


 - [ ] ID-88
Variable [MoonGame._totalSupply](contracts/MoonGame.sol#L27) is not in mixedCase

contracts/MoonGame.sol#L27


 - [ ] ID-89
Parameter [MoonGame.setDistributionCriteria(uint256,uint256)._minPeriod](contracts/MoonGame.sol#L374) is not in mixedCase

contracts/MoonGame.sol#L374


 - [ ] ID-90
Parameter [MoonGame.setAutoBuybackSettings(bool,uint256,uint256,uint256)._amount](contracts/MoonGame.sol#L300) is not in mixedCase

contracts/MoonGame.sol#L300


## similar-names
Impact: Informational
Confidence: Medium
 - [ ] ID-91
Variable [IDEXRouter.addLiquidity(address,address,uint256,uint256,uint256,uint256,address,uint256).amountADesired](contracts/IDEXRouter.sol#L10) is too similar to [IDEXRouter.addLiquidity(address,address,uint256,uint256,uint256,uint256,address,uint256).amountBDesired](contracts/IDEXRouter.sol#L11)

contracts/IDEXRouter.sol#L10


## too-many-digits
Impact: Informational
Confidence: Medium
 - [ ] ID-92
[MoonGame.slitherConstructorVariables()](contracts/MoonGame.sol#L14-L404) uses literals with too many digits:
	- [distributorGas = 500000](contracts/MoonGame.sol#L73)

contracts/MoonGame.sol#L14-L404


## unused-state
Impact: Informational
Confidence: High
 - [ ] ID-93
[MoonGame.DEAD_NON_CHECKSUM](contracts/MoonGame.sol#L21) is never used in [MoonGame](contracts/MoonGame.sol#L14-L404)

contracts/MoonGame.sol#L21


## constable-states
Impact: Optimization
Confidence: High
 - [ ] ID-94
[MoonGame._totalSupply](contracts/MoonGame.sol#L27) should be constant

contracts/MoonGame.sol#L27


 - [ ] ID-95
[MoonGame.DEAD_NON_CHECKSUM](contracts/MoonGame.sol#L21) should be constant

contracts/MoonGame.sol#L21


 - [ ] ID-96
[MoonGame.ZERO](contracts/MoonGame.sol#L20) should be constant

contracts/MoonGame.sol#L20


 - [ ] ID-97
[MoonGame.DEAD](contracts/MoonGame.sol#L19) should be constant

contracts/MoonGame.sol#L19


 - [ ] ID-98
[DividendDistributor.dividendsPerShareAccuracyFactor](contracts/DividendDistributor.sol#L28) should be constant

contracts/DividendDistributor.sol#L28


