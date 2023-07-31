https://web.archive.org/web/20210622172235/https://docs.pantherswap.com/tokenomics/referral-program

Basic Information
Token Name: PantherToken
Token Symbol: PANTHER
Contract Address: 0x1f546ad641b56b86fd9dceac473d1c7a357276b7​
Chain: Binance Smart Chain (BEP20)
Max Supply: Unlimited
Transfer Tax
Burn Rate: 2% of transfer tax will be burned immediately
Automatic Liquidity Rate: 1% of transfer tax will be added to the LP pool and locked.
Total Transfer Tax Rate: 2% of every transfer



​Automatic Liquidity
As mentioned previously, there is a 2% transfer tax on each transaction, the 1% transfer tax will be added to the PANTHER-BNB liquidity pool through the contract automatically. 
Before we launch our own AMM dex, the liquidity will be added on PancakeSwap then on PantherSwap.
Update (2021-05-11)
The router address in PantherToken has been changed to PantherSwap AMM router. It means that the 1% transfer tax will be added to the PANTHER-BNB liquidity pool.
All liquidity added by the automatic liquidity acquisition will be locked in PantherLocker contract.
The automatic liquidity which was added to PancakeSwap's liquidity pool won't be migrated to PantherSwap and also locked in PantherLocker contract.
The automatic liquidity will be transferred to PantherLocker weekly.


Automatic Burning
According to our tokenomics design, each transfer must pay a 2% transfer tax. The 1% transfer tax will be burned (sent to the black hole address) immediately.

Black Hole Address: 0x000000000000000000000000000000000000dEaD

Harvest Lockup
Harvest lockup is a unique and creative farming rewards lockup mechanism created by the PantherSwap dev team. This mechanism can help us limit the frequency of harvest to prevent farming arbitrage bots from constantly harvesting and dump.
For example, the harvest lockup of the PANTHER-BUSD farm is 2 hours. It means that farmers who stake in the PANTHER-BUSD farm can only harvest (claim their rewards from farming) every 2 hours.
You can check the harvest lockup on each farm card.
To clarify, the harvest lockup only locks users' farming rewards. The tokens and LP tokens staked in farms can be withdrawn anytime.

Anti Whale
Transfer more than 0.15% (current ratio) of the total supply will be rejected. As the total supply grows, this ratio will be reduced.
Deposit or withdraw tokens to the farms will not be subject to this restriction.


You can view the max transfer amount on our website: https://pantherswap.com, Max Tx Amount 1000


Deposit Fee Redistribution
Deposit Fee
When users enter the farming on PantherSwap, a 4% deposit fee will be charged. 
1% deposit fee will be sent to the dev team as the development fund.
3% deposit fee will be redistributed to PANTHER holders via Jungles farming.
What are Jungles?
Jungles are farming pools that allow PANTHER holders to stake their PANTHER to earn other tokens. Two jungles (BUSD & BNB) will be created by the dev team after the launch, the 3% deposit fee will be added to these two pools as the rewards for PANTHER staking.

Referral Program
An on-chain referral program has been implemented to incentivize users to invite friends to join the farming. Inviters can earn 1% of his/her friends' earnings forever.
Visit PantherSwap referral program page: https://pantherswap.com/referrals​
Unlock your wallet to get your unique referral link
Share your referral link with your friends
Every time your friends get rewards from farms, you will receive referral commissions automatically
The current referral commission rate is 1%


Community Driven
PantherDAO will be released 2 months after the initial launch. A minimum of 10,000 PANTHER is required to create new community proposals. The PantherDAO is formed to represent the will of the PANTHER community, acting in their best interests.