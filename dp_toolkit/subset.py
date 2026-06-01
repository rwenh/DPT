from __future__ import annotations
from typing import List, Optional, Tuple
from .base import DPSolver
from .decorators import memoize


class SubsetSum(DPSolver):
    """
    Subset Sum - does any subset of nums sum to exactly target?
    Returns (found: bool, subset: List[int] | None).
    """

    # ── Memoization ────────────────────────────────────────────────────────

    def solve_memo(
            self, nums: List[int], target: int
    ) -> Tuple[bool, Optional[List[int]]]:
        n = len(nums)

        @memoize
        def _dp(i: int, rem: int) -> bool:
            """Can nums[i:] produce exactly rem?"""
            if rem == 0:
                return True
            if i == n or rem < 0:
                return False
            return _dp(i + 1, rem - nums[i]) or _dp(i + 1, rem)

        found = _dp(0, target)
        subset = self._traceback(_dp, nums, target, n) if found else None
        return found, subset

    def _traceback(
            self, dp_fn, nums: List[int], target: int, n: int
    ) -> List[int]:
        chosen, rem = [], target
        for i in range(n):
            if rem == 0:
                break
            if nums[i] <= rem and dp_fn(i + 1, rem - nums[i]):
                chosen.append(nums[i])
                rem -= nums[i]
        return chosen

    # ── Tabulation ─────────────────────────────────────────────────────────

    def solve_tab(
            self, nums: List[int], target: int
    ) -> Tuple[bool, Optional[List[int]]]:
        n = len(nums)
        dp = [[False] * (target + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = True

        for i in range(1, n + 1):
            for t in range(target + 1):
                dp[i][t] = dp[i - 1][t]
                if nums[i - 1] <= t:
                    dp[i][t] = dp[i][t] or dp[i - 1][t - nums[i - 1]]

        if not dp[n][target]:
            return False, None

        chosen, t = [], target
        for i in range(n, 0, -1):
            if not dp[i - 1][t]:
                chosen.append(nums[i - 1])
                t -= nums[i - 1]
        return True, sorted(chosen)

    def table(self, nums: List[int], target: int) -> List[List[bool]]:
        """Return the full DP boolean table."""
        n = len(nums)                                   # FIX: len not lens, correct indent
        dp = [[False] * (target + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = True
        for i in range(1, n + 1):
            for t in range(target + 1):
                dp[i][t] = dp[i - 1][t]
                if nums[i - 1] <= t:
                    dp[i][t] = dp[i][t] or dp[i - 1][t - nums[i - 1]]
        return dp


class CoinChange(DPSolver):
    """
    Coin Change - fewest coins to reach amount (coins reusable).
    Returns (count, coins_used) or (-1, []) if impossible.
    """

    # ── Memoization ────────────────────────────────────────────────────────

    def solve_memo(
            self, coins: List[int], amount: int
    ) -> Tuple[int, List[int]]:                         # FIX: int not intl
        INF = float("inf")

        @memoize
        def _dp(rem: int) -> float:
            """Fewest coins to make exactly rem."""
            if rem == 0:
                return 0
            best: float = INF
            for c in coins:
                if c <= rem:
                    sub = _dp(rem - c)
                    if sub < INF:
                        best = min(best, sub + 1)
            return best

        result = _dp(amount)
        if result == INF:
            return -1, []
        return int(result), self._traceback(_dp, coins, amount)

    def _traceback(
            self, dp_fn, coins: List[int], amount: int
    ) -> List[int]:
        used, rem = [], amount
        while rem > 0:
            for c in sorted(coins):
                if c <= rem and dp_fn(rem - c) == dp_fn(rem) - 1:
                    used.append(c)
                    rem -= c
                    break
        return sorted(used)

    # ── Tabulation ─────────────────────────────────────────────────────────

    def solve_tab(
            self, coins: List[int], amount: int
    ) -> Tuple[int, List[int]]:
        INF = float("inf")
        dp = [INF] * (amount + 1)
        dp[0] = 0
        last: List[int] = [-1] * (amount + 1)

        for a in range(1, amount + 1):
            for c in coins:
                if c <= a and dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1
                    last[a] = c

        if dp[amount] == INF:
            return -1, []

        used, a = [], amount
        while a > 0:
            used.append(last[a])
            a -= last[a]
        return int(dp[amount]), sorted(used)
