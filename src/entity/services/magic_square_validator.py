"""마방진 검증 서비스."""

from src.entity.constants import GRID_SIZE, MAGIC_CONSTANT


def _sum_col(grid: list[list[int]], col: int) -> int:
    return sum(grid[r][col] for r in range(GRID_SIZE))


def _sum_main_diag(grid: list[list[int]]) -> int:
    return sum(grid[i][i] for i in range(GRID_SIZE))


def _sum_anti_diag(grid: list[list[int]]) -> int:
    return sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE))


def is_magic_square(grid: list[list[int]]) -> bool:
    """입력 격자가 4x4 마방진인지 검증한다.

    Args:
        grid: 검증 대상 격자.

    Returns:
        모든 행/열/대각선 합이 MAGIC_CONSTANT면 True, 아니면 False.
    """
    if len(grid) != GRID_SIZE:
        return False
    if any(len(row) != GRID_SIZE for row in grid):
        return False

    expected_values = set(range(1, GRID_SIZE * GRID_SIZE + 1))
    values = [value for row in grid for value in row]
    if set(values) != expected_values or len(values) != len(set(values)):
        return False

    if any(sum(row) != MAGIC_CONSTANT for row in grid):
        return False

    if any(_sum_col(grid, col) != MAGIC_CONSTANT for col in range(GRID_SIZE)):
        return False

    return (
        _sum_main_diag(grid) == MAGIC_CONSTANT
        and _sum_anti_diag(grid) == MAGIC_CONSTANT
    )
