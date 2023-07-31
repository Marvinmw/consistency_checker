## whitepaper

### Item v0

   &ensp;**info**
   &emsp; 
- Description: 
    TRADING FEES. Biokript exchange will charge a 0.20% fee for both Makers and Takers. Users holding our Biokript tokens will automatically get a discount.
     
   - Possible Var Names from ChatGPT: ['tradingFee', 'exchangeFee', 'bktFee'] 
   - Expression:  0.002 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = _fee

   &ensp;**isEq**
    Eq(_fee, 2.0)

### Item v1

   &ensp;**info**
   &emsp; 
- Description: 
    WITHDRAWAL FEE. We charge a small fee for withdrawals and this fee is dynamic depending how busy is the network
     
   - Possible Var Names from ChatGPT: ['withdrawalFee', 'dynamicWithdrawalFee', 'networkWithdrawalFee'] 
   - Expression:  None 


   &ensp;**claim**
    not defined the value in the whitepaper

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = _fee

   &ensp;**isEq**
    False

### Item v2

   &ensp;**info**
   &emsp; 
- Description: 
  CREDIT OR DEBIT CARD PURCHASES. We will also charge a small fee for credit or debit card purchases.
     
   - Possible Var Names from ChatGPT: ['cardPurchaseFee', 'paymentCardFee', 'transactionCardFee'] 
   - Expression:  None 


   &ensp;**claim**
    not defined the value in the whitepaper

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = _fee

   &ensp;**isEq**
    False

### Item v3

   &ensp;**info**
   &emsp; 
- Description: 
   LISTING FEE. We are very selective in coins we choose to be on our platform, and we charge projects a fee to list their token on our exchange. Before the listing, there is a detailed analysis of the project to make sure the project complies with all the security regulations of our exchange.
     
   - Possible Var Names from ChatGPT: ['listingFee', 'tokenListingFee', 'projectListingFee'] 
   - Expression:  None 


   &ensp;**claim**
    not defined the value in the whitepaper

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = _fee

   &ensp;**isEq**
    False

### Item v4

   &ensp;**info**
   &emsp; 
- Description: 
   VOTING FEES. To engage our community with our platform, we’ll also have a voting fee in order to list a token. That is a very popular and engaging way to include our community in the listing process on our platform.
     
   - Possible Var Names from ChatGPT: ['votingFee', 'tokenVotingFee', 'communityVotingFee'] 
   - Expression:  None 


   &ensp;**claim**
    not defined the value in the whitepaper

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = _fee

   &ensp;**isEq**
    False

### Item v5

   &ensp;**info**
   &emsp; 
- Description: 
  10% of all trading fee revenues  will be set aside for token burn, and for every 100% BKPT appreciation, we’ll start with a 1% burn of the entire token supply. 
     
   - Possible Var Names from ChatGPT: ['burnFee', 'revenueBurn', 'appreciationBurn'] 
   - Expression:  0.1 


   &ensp;**Is the fee found**
    No

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = _fee

   &ensp;**isEq**
    Eq(_fee, 10.0)

### Item v6

   &ensp;**info**
   &emsp; 
- Description: 
There is always a buyer and a seller, so the exchange will always collect trade fees from both of them.
     
   - Possible Var Names from ChatGPT: ['tradeFee', 'buyerSellerFee', 'exchangeCommission'] 
   - Expression:  None 


   &ensp;**claim**
    not defined the value in the whitepaper

   &ensp;**matched_var_name**
    liquidityFee

   &ensp;**matched_var_exp**
    liquidityFee = _fee

   &ensp;**isEq**
    False


## hidden_fee_function


## hidden_fee_var

### liquidityFee

  &ensp;** Possible Values **:
 _fee

### _isExcludedFromFees_account_

  &ensp;** Possible Values **:
 excluded

### liqFee

  &ensp;** Possible Values **:
 _amount*liquidityFee/100, 
 0, 
 _amount*liquidityFee/100, 
 _amount*liquidityFee/100, 
 _amount*liquidityFee/100, 
 0


