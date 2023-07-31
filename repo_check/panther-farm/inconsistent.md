PTC-01 | Inconsistent Burn Rate
Category Severity Location Status
Inconsistency Minor PantherToken.sol: 15~16 Partially Resolved
Description
In the whitepaper, the burn rate is 3%, where as in the code, it is initialized as 1%.
15 // Burn rate % of transfer tax. (default 20% x 5% = 1% of total amount).
16 uint16 public burnRate = 20;
Recommendation
We recommend reconciling the burn rate in the whitepaper and the code.
Alleviation
[PantherSwap Team]: The burnRate can be updated in the PantherToken.updateBurnRate() .