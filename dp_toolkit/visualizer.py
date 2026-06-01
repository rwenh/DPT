from __future__ import annotations
from typing import Any, List, Optional

def print_table(
        table: List[List[Any]],
        *,
        row_labels: Optional[List[str]] = None,
        col_labels: Optional[List[str]] = None,
        title: str = "DP Table",
        max_cols: int = 16,
) -> None:
    """
    Pretty-print a 2D DP table with optional row/column labels.
    Handles int, float (shows ∞), and bool (shows T/F) cell values.
    Truncates wide tables to max_cols columns.
    """
    cols = min(len(table[0]) if table else 0, max_cols)

    label_w = max((len(r) for r in (row_labels or [])), default=1) + 1
    cell_w  = 4

    total_w = label_w + 3 + cols * (cell_w + 1)        # FIX: total_w not total_2, correct formula
    sep = "-" * total_w                                 # FIX: total_w now defined

    print(f"\n {title}")
    print(f" {sep}")

    if col_labels:
        header = " " * (label_w + 3)
        for j in range(cols):
            header += col_labels[j].rjust(cell_w) + " "
        if len(table[0]) > max_cols:                    # FIX: these 3 lines moved outside for loop
            header += " ..."
        print(f" {header}")
        print(f" {sep}")

    for i, row in enumerate(table):
        lbl   = (row_labels[i] if row_labels else str(i)).rjust(label_w)
        cells = ""
        for j in range(cols):
            v = row[j]
            if v is True:
                display = "T"
            elif v is False:
                display = "F"
            elif v == float("inf"):
                display = "∞"
            else:
                display = str(v)
            cells += display.rjust(cell_w) + " "        # FIX: rjust not rjusat, correct indent
        if len(row) > max_cols:
            cells += "..."
        print(f" {lbl} | {cells}")
    print(f" {sep}\n")


OP_SYMBOL = {
    "match":   ".",
    "replace": "~",
    "delete":  "-",
    "insert":  "+",
}

def print_ops(ops: list, title: str = "Operations") -> None:  # FIX: list not lsit
    """Print edit-distance operations with symbolic indicators."""
    print(f" {title}:")
    for op, detail in ops:
        sym = OP_SYMBOL.get(op, "?")                    # FIX: op not opo
        print(f"  [{sym}] {op:8s} {detail}")
    print()
