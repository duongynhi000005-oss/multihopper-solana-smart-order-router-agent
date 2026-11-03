#!/usr/bin/env python3
"""MultiHopper Solana Smart Order Router (SOR) & Convex Split Solver."""
from dataclasses import dataclass
from typing import List, Dict

MAX_SOLANA_CU = 1_400_000
MAX_ALT_ACCOUNTS = 64

@dataclass
class PoolLeg:
    dex: str
    pool_id: str
    token_in: str
    token_out: str
    reserve_in: float
    reserve_out: float
    fee_bps: float
    cu_estimate: int
    accounts_required: int

    def quote_out(self, amount_in: float) -> float:
        if amount_in <= 0 or self.reserve_in <= 0 or self.reserve_out <= 0:
            return 0.0
        eff_in = amount_in * (1.0 - self.fee_bps / 10_000.0)
        return (self.reserve_out * eff_in) / (self.reserve_in + eff_in)

def optimize_split_route(legs: List[PoolLeg], total_amount_in: float, steps: int = 20) -> Dict:
    allocations = {leg.pool_id: 0.0 for leg in legs}
    chunk = total_amount_in / steps
    used_cu = 45_000
    used_accounts = 8
    active_pools = set()

    for _ in range(steps):
        best_leg = None
        best_marginal_out = -1.0
        for leg in legs:
            add_cu = 0 if leg.pool_id in active_pools else leg.cu_estimate
            add_acc = 0 if leg.pool_id in active_pools else leg.accounts_required
            if used_cu + add_cu > MAX_SOLANA_CU or used_accounts + add_acc > MAX_ALT_ACCOUNTS:
                continue
            cur_in = allocations[leg.pool_id]
            marginal = leg.quote_out(cur_in + chunk) - leg.quote_out(cur_in)
            if marginal > best_marginal_out:
                best_marginal_out = marginal
                best_leg = leg
        if best_leg:
            if best_leg.pool_id not in active_pools:
                active_pools.add(best_leg.pool_id)
                used_cu += best_leg.cu_estimate
                used_accounts += best_leg.accounts_required
            allocations[best_leg.pool_id] += chunk

    total_out = sum(leg.quote_out(allocations[leg.pool_id]) for leg in legs)
    return {
        "total_amount_in": total_amount_in,
        "total_amount_out": round(total_out, 6),
        "total_cu_used": used_cu,
        "total_accounts_used": used_accounts,
        "splits": {k: round(v, 4) for k, v in allocations.items() if v > 0},
    }

if __name__ == "__main__":
    sample_legs = [
        PoolLeg("Meteora DLMM", "met_sol_usdc", "SOL", "USDC", 25000, 4500000, 15, 110000, 14),
        PoolLeg("Raydium CLMM", "ray_sol_usdc", "SOL", "USDC", 40000, 7200000, 25, 95000, 12),
        PoolLeg("Orca Whirlpool", "orca_sol_usdc", "SOL", "USDC", 18000, 3240000, 20, 88000, 11),
    ]
    print(optimize_split_route(sample_legs, 1500.0))
