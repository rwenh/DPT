from __future__ import annotations
from typing import List, Tuple
from .base import DPSolver
from .decorators import memoize

# (op_name, detail) e.g. ("replace", "k->s") or ("match", "i")
Op = Tuple[str, str]                                    # FIX: Op not op


class LCS(DPSolver):
    """
    Longest Common Subsequence.
    Returns (length, subsequence_string).
    """

    # ── Memoization ────────────────────────────────────────────────────────

    def solve_memo(self, s1: str, s2: str) -> Tuple[int, str]:
        m, n = len(s1), len(s2)                         # FIX: m, n not n, n

        @memoize
        def _dp(i: int, j: int) -> int:
            """LCS length for s1[i:] and s2[j:]."""
            if i == m or j == n:
                return 0
            if s1[i] == s2[j]:
                return 1 + _dp(i + 1, j + 1)
            return max(_dp(i + 1, j), _dp(i, j + 1))

        length = _dp(0, 0)
        seq = self._traceback_memo(_dp, s1, s2, m, n)
        return length, seq

    def _traceback_memo(
            self, dp_fn, s1: str, s2: str, m: int, n: int
    ) -> str:
        result = []
        i = j = 0
        while i < m and j < n:
            if s1[i] == s2[j]:
                result.append(s1[i])
                i += 1; j += 1
            elif dp_fn(i + 1, j) >= dp_fn(i, j + 1):
                i += 1
            else:
                j += 1
        return "".join(result)                          # FIX: dedented out of else block

    # ── Tabulation ─────────────────────────────────────────────────────────

    def solve_tab(self, s1: str, s2: str) -> Tuple[int, str]:
        m, n = len(s1), len(s2)
        # dp[i][j] = LCS length of s1[:i] and s2[:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        seq = []
        i, j = m, n
        while i > 0 and j > 0:
            if s1[i - 1] == s2[j - 1]:
                seq.append(s1[i - 1])
                i -= 1; j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        return dp[m][n], "".join(reversed(seq))         # FIX: dedented out of else block


class EditDistance(DPSolver):
    """
    Levenshtein Edit Distance (insert, delete, replace).
    Returns (distance, list_of_operations).
    Operations: ("match"|"replace"|"delete"|"insert", detail_string)
    """

    # ── Memoization ────────────────────────────────────────────────────────

    def solve_memo(self, s1: str, s2: str) -> Tuple[int, List[Op]]:
        m, n = len(s1), len(s2)

        @memoize
        def _dp(i: int, j: int) -> int:
            """Min edits to convert s1[i:] into s2[j:]."""
            if i == m:
                return n - j
            if j == n:
                return m - i
            if s1[i] == s2[j]:
                return _dp(i + 1, j + 1)
            return 1 + min(
                _dp(i + 1, j),
                _dp(i, j + 1),
                _dp(i + 1, j + 1),
            )

        dist = _dp(0, 0)
        ops = self._traceback_memo(_dp, s1, s2, m, n)
        return dist, ops

    def _traceback_memo(
            self, dp_fn, s1: str, s2: str, m: int, n: int
    ) -> List[Op]:
        ops: List[Op] = []
        i = j = 0
        while i < m or j < n:
            if i == m:
                ops.append(("insert", s2[j])); j += 1
            elif j == n:
                ops.append(("delete", s1[i])); i += 1
            elif s1[i] == s2[j]:
                ops.append(("match", s1[i])); i += 1; j += 1
            else:
                d   = dp_fn(i + 1, j)
                ins = dp_fn(i, j + 1)
                rep = dp_fn(i + 1, j + 1)
                best = min(d, ins, rep)                 # FIX: best was never assigned
                if rep == best:
                    ops.append(("replace", f"{s1[i]}->{s2[j]}")); i += 1; j += 1
                elif d == best:
                    ops.append(("delete", s1[i])); i += 1
                else:
                    ops.append(("insert", s2[j])); j += 1
        return ops                                      # FIX: dedented out of while loop

    # ── Tabulation ─────────────────────────────────────────────────────────

    def solve_tab(self, s1: str, s2: str) -> Tuple[int, List[Op]]:  # FIX: unindented - own method
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1): dp[i][0] = i
        for j in range(n + 1): dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:             # FIX: was truncated
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],
                        dp[i][j - 1],
                        dp[i - 1][j - 1],
                    )

        ops: List[Op] = []
        i, j = m, n
        while i > 0 or j > 0:
            if i == 0:
                ops.append(("insert", s2[j - 1])); j -= 1
            elif j == 0:
                ops.append(("delete", s1[i - 1])); i -= 1
            elif s1[i - 1] == s2[j - 1]:
                ops.append(("match", s1[i - 1])); i -= 1; j -= 1
            elif dp[i][j] == 1 + dp[i - 1][j - 1]:
                ops.append(("replace", f"{s1[i-1]}->{s2[j-1]}")); i -= 1; j -= 1
            elif dp[i][j] == 1 + dp[i - 1][j]:
                ops.append(("delete", s1[i - 1])); i -= 1
            else:
                ops.append(("insert", s2[j - 1])); j -= 1

        return dp[m][n], list(reversed(ops))
