HFT-03 | The 2500 BNB MAX_BNB_TO_ADD_TO_LP is inconsistent with 2200 BNB
maxTokensToAddToLiquidity in the whitepaper
Category Severity Location Status
Volatile Code Medium HFTtoken.sol (1): 746, 1264, 713 Resolved
Description
According to the description in Hodl Finance smart contract details.
maxTokensToAddToLiquidity = 2500 BNB To avoid becoming a stable coin we want a max of approx. 2m
automatically added to the LP This is 50% HFT and 50% BNB. We cant calculate $value so we pegged
BNB at $400.
So we decided 2500 BNB would be a great middle and we can always add manually.
But the MAX_BNB_TO_ADD_TO_LP is a fixed number 2200 * 10**18 (2200 BNB) without any interface for
adding manually after deploying.
Recommendation
We recommend updating the MAX_BNB_TO_ADD_TO_LP to make it consistent with the white paper.
Alleviation
[HODL Team]: There are 300BNB initial + 2200BNB added from 2% tax on each transaction would be
added to the marketing treasury.

HFT-04 | The numTokensSellToAddToLiquidity is inconsistent with the whitepaper
Category Severity Location Status
Inconsistency Medium HFTtoken.sol (1): 715, 748, 1261~1262 Resolved
Description
According to the description in Hodl Finance smart contract details.
Add liquidity function This is done every 1 million HFT instead of every transaction.
numTokensSellToAddToLiquidity = 1 * 10*6 * 10*9
But the implementation defines NUM_TOKENS_SELL_TO_ADD_TO_LP = 10 * 10**6 * 10**9
Recommendation
We suggest update the NUM_TOKENS_SELL_TO_ADD_TO_LP to make it consistent with white paper.
Alleviation
[HODL Team]: Updated the document.