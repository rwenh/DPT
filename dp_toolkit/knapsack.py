from __future__ import annotations
from typing import List, Tuple
from .base import DPSolver
from .decorators import memoize

class Knapsack01(DPSolver):
    """
    0/1 Knapsack - each item used at most once.
    Returns (max_value, selected_item_indices)
    """

    # ── Memoization ────────────────────────────────────────────────────────

    def solve_memo(
            self,
            weights: List[int],
            values: List[int],
            capacity: int,
    ) -> Tuple[int, List[int]]:                        # FIX: dot → comma
        n = len(weights)

        @memoize
        def _dp(i: int, cap: int) -> int:
            """Max value using items[i:] with remaining capacity cap."""
            if i == n or cap == 0:
                return 0
            if weights[i] > cap:
                return _dp(i + 1, cap)
            return max(
                _dp(i + 1, cap),
                values[i] + _dp(i + 1, cap - weights[i])
            )

        best = _dp(0, capacity)
        items = self._traceback_memo(_dp, weights, values, capacity, n)
        return best, items

    def _traceback_memo(
            self, dp_fn, weights: List[int], values: List[int], capacity: int, n: int
    ) -> List[int]:
        chosen, cap = [], capacity
        for i in range(n):
            if cap == 0:
                break
            skip = dp_fn(i + 1, cap)
            take = (
                values[i] + dp_fn(i + 1, cap - weights[i])
                if weights[i] <= cap else -1
            )
            if take > skip:
                chosen.append(i)
                cap -= weights[i]
        return chosen

    # ── Tabulation ─────────────────────────────────────────────────────────

    def solve_tab(
            self,
            weights: List[int],
            values: List[int],
            capacity: int,
    ) -> Tuple[int, List[int]]:
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            w, v = weights[i - 1], values[i - 1]
            for c in range(capacity + 1):
                dp[i][c] = dp[i - 1][c]
                if w <= c:
                    dp[i][c] = max(dp[i][c], v + dp[i - 1][c - w])

        chosen, c = [], capacity
        for i in range(n, 0, -1):
            if dp[i][c] != dp[i - 1][c]:
                chosen.append(i - 1)
                c -= weights[i - 1]
        return dp[n][capacity], sorted(chosen)

    # ── Utilities ──────────────────────────────────────────────────────────

    def table(
            self, weights: List[int], values: List[int], capacity: int
    ) -> List[List[int]]:
        """Return the full DP table (rows = items, cols = capacity)."""  # FIX: indented
        n = len(weights)                                                  # FIX: indented
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            w, v = weights[i - 1], values[i - 1]
            for c in range(capacity + 1):
                dp[i][c] = dp[i - 1][c]                # FIX: removed duplicate if/assign
                if w <= c:
                    dp[i][c] = max(dp[i][c], v + dp[i - 1][c - w])
        return dp                                       # FIX: moved outside for loop


class UnboundedKnapsack(DPSolver):
    """
    Unbounded Knapsack - each item may be used any number of times.
    Returns the maximum value achievable within capacity.
    """

    def solve_memo(
            self, weights: List[int], values: List[int], capacity: int  # FIX: List not Lists
    ) -> int:
        @memoize
        def _dp(cap: int) -> int:
            if cap == 0:
                return 0
            best = 0
            for i, w in enumerate(weights):
                if w <= cap:
                    best = max(best, values[i] + _dp(cap - w))
            return best
        return _dp(capacity)

    def solve_tab(                                      # FIX: added missing solve_tab
            self, weights: List[int], values: List[int], capacity: int
    ) -> int:
        dp = [0] * (capacity + 1)
        for c in range(1, capacity + 1):
            for i, w in enumerate(weights):
                if w <= c:
                    dp[c] = max(dp[c], values[i] + dp[c - w])
        return dp[capacity]
