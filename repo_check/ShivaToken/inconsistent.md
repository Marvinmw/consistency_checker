STS-14 | Inconsistency With White Paper
Category Severity Location Status
Inconsistency Minor ShivaToken.sol: 1237, 1643 Acknowledged
Description
The whitepaper for Shiva Token states that:
" After a certain amount of tokens have been stored in the contract (0.0001% of the
total supply) it initiates a swap. " However, the amount is hard coded as 20,000,000 tokens.
" The transaction limit is set to 0.1% of the total supply " However, the
maxTransferAmountRate is settable up to 6.5536% of total supply, currently 1%.
Recommendation
We recommend updating the contract or white paper to make them consistent with each other.
Alleviation
[ShivaToken Team]: acknowledged this finding