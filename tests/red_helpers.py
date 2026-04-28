from importlib import import_module
from typing import Any

import pytest


DURER_MAGIC_SQUARE: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def copy_grid(grid: list[list[int]]) -> list[list[int]]:
    return [row[:] for row in grid]


def load_attr(module_path: str, attr_name: str) -> Any:
    try:
        module = import_module(module_path)
    except Exception as exc:  # pragma: no cover - RED stage expects this
        pytest.fail(
            f"RED: module '{module_path}' import failed. "
            f"Implement module first. ({exc.__class__.__name__}: {exc})"
        )

    if not hasattr(module, attr_name):
        pytest.fail(
            f"RED: '{module_path}.{attr_name}' is missing. "
            "Implement symbol to satisfy test contract."
        )
    return getattr(module, attr_name)
