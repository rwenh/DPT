#!/usr/bin/env python3
"""
Dynamic Programming Toolkit — Demo
Exercises all solvers with both tabulation and memoization, including
traceback, DP table visualization, and timing.
"""

from dp_toolkit import (
    Knapsack01, UnboundedKnapsack,
    LCS, EditDistance,
    SubsetSum, CoinChange,
    dp_timer, print_table, print_ops,
)

W = "═" * 54


def section(title: str) -> None:
    print(f"\n{W}")
    print(f"  {title}")
    print(W)


# ── 1. Knapsack 0/1 ───────────────────────────────────────────────────────
section("1. Knapsack 0/1")

weights = [2, 3, 4, 5]
values  = [3, 4, 5, 6]
cap     = 8
labels  = ["lantern", "compass", "map", "telescope"]
solver  = Knapsack01()

val_t, idx_t = dp_timer(solver.solve_tab)(weights, values, cap)
print(f"  Tabulation  → value={val_t}, items={[labels[i] for i in idx_t]}")

val_m, idx_m = dp_timer(solver.solve_memo)(weights, values, cap)
print(f"  Memoization → value={val_m}, items={[labels[i] for i in idx_m]}")

dp_tbl   = solver.table(weights, values, cap)
row_lbls = ["∅"] + labels
col_lbls = [f"c={c}" for c in range(cap + 1)]
print_table(dp_tbl, row_labels=row_lbls, col_labels=col_lbls, title="Knapsack 0/1 DP Table")


# ── 2. Unbounded Knapsack ─────────────────────────────────────────────────
section("2. Unbounded Knapsack")

w2 = [1, 3, 4, 5]
v2 = [1, 4, 5, 7]
c2 = 7

ub = UnboundedKnapsack()
print(f"  weights={w2}, values={v2}, capacity={c2}")
print(f"  Tabulation  → {ub.solve_tab(w2, v2, c2)}")
print(f"  Memoization → {ub.solve_memo(w2, v2, c2)}")


# ── 3. Longest Common Subsequence ─────────────────────────────────────────
section("3. Longest Common Subsequence")

s1, s2 = "ABCBDAB", "BDCABA"
lcs = LCS()

len_t, seq_t = lcs.solve_tab(s1, s2)
print(f"  s1={s1!r}  s2={s2!r}")
print(f"  Tabulation  → length={len_t}, lcs={seq_t!r}")

len_m, seq_m = lcs.solve_memo(s1, s2)
print(f"  Memoization → length={len_m}, lcs={seq_m!r}")


# ── 4. Edit Distance ──────────────────────────────────────────────────────
section("4. Edit Distance (Levenshtein)")

pairs = [("kitten", "sitting"), ("sunday", "saturday"), ("", "abc")]
ed = EditDistance()

for w1, w2 in pairs:
    dist_t, ops_t = ed.solve_tab(w1, w2)
    dist_m, _     = ed.solve_memo(w1, w2)
    print(f"  {w1!r:>10} → {w2!r:<12}  distance={dist_t}  (memo={dist_m})")
    if w1 == "kitten":                # show full op list for first pair
        print_ops(ops_t, "  Operations (kitten → sitting)")


# ── 5. Subset Sum ─────────────────────────────────────────────────────────
section("5. Subset Sum")

ss = SubsetSum()
cases = [
    ([3, 1, 4, 1, 5, 9, 2, 6], 15),
    ([1, 2, 3, 7],              6),
    ([2, 4, 6],                 7),   # impossible
]

for nums, target in cases:
    found_t, sub_t = ss.solve_tab(nums, target)
    found_m, sub_m = ss.solve_memo(nums, target)
    print(f"  nums={nums}, target={target}")
    print(f"    tab  → found={found_t}, subset={sub_t}")
    print(f"    memo → found={found_m}, subset={sub_m}")

# Boolean DP table for small example
nums_small, tgt_small = [3, 1, 4, 2], 6
tbl = ss.table(nums_small, tgt_small)
print_table(
    tbl,
    row_labels=["∅"] + [str(n) for n in nums_small],
    col_labels=[str(t) for t in range(tgt_small + 1)],
    title=f"SubsetSum table  nums={nums_small}  target={tgt_small}",
)


# ── 6. Coin Change ────────────────────────────────────────────────────────
section("6. Coin Change")

cc = CoinChange()
cases_cc = [
    ([1, 5, 6, 9], 11),   # optimal: 5+6
    ([1, 2, 5],    11),   # optimal: 5+5+1
    ([3, 7],       11),   # impossible
    ([2],           3),   # impossible
]

for coins, amount in cases_cc:
    cnt_t, used_t = cc.solve_tab(coins, amount)
    cnt_m, used_m = cc.solve_memo(coins, amount)
    print(f"  coins={coins}, amount={amount}")
    print(f"    tab  → count={cnt_t}, used={used_t}")
    print(f"    memo → count={cnt_m}, used={used_m}")


# ── Decorator showcase ────────────────────────────────────────────────────
section("7. Memoize decorator — cache stats")

from dp_toolkit import memoize

@memoize
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(30)
print(f"  fib(30) = {fib(30)}")
print(f"  cache   = {fib.cache_info()}")

fib.cache_clear()
print(f"  after clear: {fib.cache_info()}")


print(f"\n{W}")
print("  All solvers complete ✓")
print(W)
