from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class DPSolver(ABC):
    """
    Abstract base for all DP solvers.

    Subclasses implement both solve_memo() (top-down) and solve_tab() (bottom-up).
    Dispatch via .solve(*args, method='tab'|'memo').
    """

    def solve(self, *args: Any, method: str = "tab", **kwargs: Any) -> Any:
        """Route to tabulation or memoization based on `method`."""
        if method == "memo":
            return self.solve_memo(*args, **kwargs)
        return self.solve_tab(*args, **kwargs)

    @abstractmethod
    def solve_memo(self, *args: Any, **kwargs: Any) -> Any:
        """Top-down recursive solution with memoization."""

    @abstractmethod
    def solve_tab(self, *args: Any, **kwargs: Any) -> Any:
        """Bottom-up iterative solution with tabulation."""
