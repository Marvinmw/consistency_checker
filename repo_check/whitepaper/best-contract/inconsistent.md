BEF-01 | The Difference Between Implementation and White Paper on
Token Initial Circulation
Category Severity Location Status
Logical Issue Minor token_best.sol: 216~219 Declined
Description
The white paper(https://bestokens.network/BEST_Whitepaper.pdf) wrote that its initial circulation is
180,000 BEST, but the implementation implies that its initial circulation is 5,000,000 BEST.
216 constructor () public ERC20Detailed("Bitcoin And Ethereum Standard Token", "BEST",
6) {
217 decimalVal = 10 ** 6;
218 _mint(msg.sender, 5000000*decimalVal);
219 }
Alleviation
No alleviation.


BEO-01 | The Difference Between Implementation and White Paper
Category Severity Location Status
Logical Issue Informational best_pool.sol: 136~137 Resolved
Description
The white paper(https://bestokens.network/BEST_Whitepaper.pdf) wrote that "BEST tokens staked on the
official website will be unlocked linearly in 12 weeks, and 1/12 will be unlocked per week.", however, the
code's implementation below implies that BEST tokens will be unlocked per 3 minutes.
136 uint public FreezeTime = 3 minutes;
137 uint public UnfreezePercent = 12; // 1/12
Recommendation
Consider keeping the code's implementation and the description of white paper the same.
Alleviation
The development team resolved this issue in the file of zip file whose shasum value is
e001424a95af462ce816f9f53db2a80480187ee11a2bf84f36815aecd0a3f313.

BEI-01 | The Difference Between Implementation and White Paper on
Token Initial Circulation
Category Severity Location Status
Logical Issue Minor token_musk.sol: 216~219 Declined
Description
The white paper(https://bestokens.network/BEST_Whitepaper.pdf) wrote that its daily initial circulation is
40,000 MUSK, but the implementation implies that its initial circulation is 10,000,000 MUSK.
216 constructor () public ERC20Detailed("MUSK", "MUSK", 6) {
217 decimalVal = 10 ** 6;
218 _mint(msg.sender, 10000000*decimalVal);
219 }
Alleviation
No alleviation.
