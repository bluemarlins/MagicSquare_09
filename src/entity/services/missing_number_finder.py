"""누락 숫자 탐색 서비스."""

from src.entity.constants import GRID_SIZE


def find_not_exist_nums(grid: list[list[int]]) -> list[int]:
    """격자에 없는 숫자를 오름차순으로 반환한다.

    Args:
        grid: 4x4 입력 격자.

    Returns:
        1..(GRID_SIZE^2) 범위에서 누락된 숫자 목록.
    """
    upper_bound = GRID_SIZE * GRID_SIZE
    present = {
        value
        for row in grid
        for value in row
        if isinstance(value, int) and value != 0
    }
    return [num for num in range(1, upper_bound + 1) if num not in present]
