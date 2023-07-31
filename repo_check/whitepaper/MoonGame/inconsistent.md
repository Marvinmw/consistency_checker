MGM-03 | Inconsistent Value of _maxTxAmount
Category Severity Location Status
Inconsistency Informational projects/MoonGame/contracts/MoonGame.sol (dc1a72a): 28 Acknowledged
Description
28 uint256 public _maxTxAmount = _totalSupply.div(200); // 0.25%
Variable _maxTxAmount is set to 0.5% of _totalSupply , but the comment says 0.25%.
Moreover, on the whitepaper, "The anti-whale mechanic disallows sellers to offload more than 0.1% of the
entire supply of the token."
Recommendation
We recommend revising the code, the comment, and the whitepaper to eliminate the inconsistency.
Alleviation
The team has acknowledged the finding.


MGM-06 | Charging Additional Fees
Category Severity Location Status
Inconsistency Major projects/MoonGame/contracts/MoonGame.sol (dc1a72a): 193, 196 Acknowledged
Description
191 function getMultipliedFee() public returns (uint256) {
192 if (launchedAtTimestamp + 1 days > block.timestamp) {
193 return totalFee.mul(18000).div(feeDenominator);
194 } else if (buybackMultiplierTriggeredAt.add(buybackMultiplierLength) >
block.timestamp) {
195 uint256 remainingTime =
buybackMultiplierTriggeredAt.add(buybackMultiplierLength).sub(block.timestamp);
196 uint256 feeIncrease =
totalFee.mul(buybackMultiplierNumerator).div(buybackMultiplierDenominator).sub(totalFee);
197 return
totalFee.add(feeIncrease.mul(remainingTime).div(buybackMultiplierLength));
198 }
199 return totalFee;
200 }
The contract charges an additional 18% fee for selling tokens within one day after being launched.
Else, the contract charges an additional fee (the value of variable feeIncrease ) for selling tokens within
some time (the value of variable buybackMultiplierLength ) after the buyback.
Both the fees above are not shown on the whitepaper.
Recommendation
We recommend revising the code or the whitepaper to eliminate the inconsistencies.
Alleviation
The team has acknowledged the finding.