pragma solidity 0.6.11;
'''
直接从白皮书里翻译成代码，不考虑公示直接的互相引用
'''
contract Equations{
    // uint256 public total_ava_liquidity;
    // unint256 public borrow_amount;
    // mapping(address => uint ) public borrow_list;
  
    function getTotalLiquidity(uint256 total_ava_liquidity, uint256 total_borrows) view returns (uint256){
        return total_ava_liquidity + total_borrows;
    }

    function getTotalBorrows(uint256 borrow_amount, uint256 cumulative_borrow_interest) view returns (uint256){
        return borrow_amount + cumulative_borrow_interest;
    }

    function getAlTokens(uint256 deposit_amount, uint256 total_altoken, uint256 total_liquidity) view returns (uint256) {
        return deposit_amount*total_altoken/total_liquidity;
    }

    // function getAccountHealth() view returns (bool){
    //     uint borrow_vale = borrow_list[msg.sender];
    //     if (borrow_vale <= borrow_limit){
    //         return True;
    //     }else{
    //         return False;
    //     }
    // }

    function getBorrowShares(uint256 borrow_amount, uint256 total_borrow_shares, uint256 total_borrows) view returns (uint256){
        return (borrow_amount*total_borrow_shares)/total_borrows;
    }

    function withDrawShares(uint256 withdraw_amount, uint256 total_altoken, uint256 total_liquidity) view returns (uint256){
        return withdraw_amount * total_altoken / total_liquidity;
    }

    function getUtilizationRate(uint256 total_borrows, uin256 total_liquidity) view returns (uint256){
        return total_borrows/total_liquidity;
    }

    function getBorrowInterestRate1(uint256 base_borrow_rate, uint256 utilization_rate, uint256 slope1) view returns (uint256){
        return base_borrow_rate + utilization_rate * slope1;
    }

    //  function f(uint256 base_borrow_rate, uint256 utilization_rate, uint256 slope1) view returns (uint256){
    //     return Math.max(base_borrow_rate-utilization_rate, slope1)+10;
    // }

    function getBorrowInterestRate2(uint256 base_borrow_rate, uint256 utilization_rate, uint256 slope1) view returns (uint256){
        return slope1 + (utilization_rate-optimal_utilization_rate)/(1-optimal_utilization_rate) * slope2;
    }

    function getDepositInterestRate(uint256 borrow_interest_rate, uint256 utilization_rate ) view returns (uint256){
        return  borrow_interest_rate * utilization_rate;
    }

    function getCollateralAmount(uint256 liquidate_amount, uint256 price_liquidate, uint256 price_collateral_asset, unint256 liquidation_bonus) view returns (uint256){
        return (liquidate_amount * price_liquidate / price_collateral_asset) * liquidation_bonus;
    }

    function getLiquidateAmount(uint256 liquidate_share, uint256 total_borrows, uint256 total_borrow_shares) view returns (uint256){
        return (liquidate_share*total_borrows)/total_borrow_shares;
    }

    function getRepayShares(uint256 repay_amount, uint256 total_borrow_shares, uint256 total_liquidity) view returns (uint256){
        return repay_amount * total_borrow_shares / total_liquidity;
    }
}