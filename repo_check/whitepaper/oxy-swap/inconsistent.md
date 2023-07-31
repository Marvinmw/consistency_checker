ORR-03 | Incorrect Trade Fee Statement
Category Severity Location Status
Inconsistency Informational OxyRouter.sol: 723~726, 733~735 Acknowledged
Description
OxySwap Whitepaper states 'When you make a token swap (trade) on the exchange you will pay a 0.2%
trading fee, which is returned to liquidity pools in the form of a fee reward for liquidity providers.', however,
the actual trade fee is 0.3%.
Recommendation
Consider to update the document or change trade fee.
Alleviation
The team acknowledged the finding, and given the deployed contract cannot be updated, decided to
retain the code base unchanged.