from __future__ import annotations
import functools
import time
from typing import Any, Callable


def memoize(func: Callable) -> Callable:
    """
    Cache results of recursive DP calls with hit/miss tracking.

    Attaches .cache_info() and .cache_clear() to the wrapper.
    Note: each call to the enclosing solve_memo() creates a fresh cache,
    so memoization is scoped to a single problem invocation.
    """
    cache: dict[tuple, Any] = {}
    stats = {"hits": 0, "misses": 0}

    @functools.wraps(func)
    def wrapper(*args: Any) -> Any:
        if args in cache:
            stats["hits"] += 1
            return cache[args]
        stats["misses"] += 1
        result = func(*args)
        cache[args] = result
        return result

    wrapper.cache = cache                                          # type: ignore[attr-defined]
    wrapper.cache_info = lambda: {**stats, "size": len(cache)}    # type: ignore[attr-defined]
    wrapper.cache_clear = lambda: (cache.clear(),                  # type: ignore[attr-defined]
                                   stats.update({"hits": 0, "misses": 0}))
    return wrapper


def dp_timer(func: Callable) -> Callable:
    """Print wall-clock time for any DP solve call."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        print(f"  ⏱  {func.__qualname__}: {elapsed_ms:.3f} ms")
        return result
    return wrapper
