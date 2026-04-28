"""마방진 검증 서비스."""

from src.entity.constants import GRID_SIZE, MAGIC_CONSTANT


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

    for row in grid:
        if sum(row) != MAGIC_CONSTANT:
            return False

    for col in range(GRID_SIZE):
        if sum(grid[row][col] for row in range(GRID_SIZE)) != MAGIC_CONSTANT:
            return False

    main_diagonal = sum(grid[idx][idx] for idx in range(GRID_SIZE))
    anti_diagonal = sum(grid[idx][GRID_SIZE - 1 - idx] for idx in range(GRID_SIZE))
    return main_diagonal == MAGIC_CONSTANT and anti_diagonal == MAGIC_CONSTANT
