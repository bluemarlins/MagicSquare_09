"""빈칸 좌표 탐색 서비스."""

from src.constants import BLANK_COUNT, BLANK_MARKER
from src.exceptions.domain_exceptions import InvalidBlankCountError


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """row-major 순서로 빈칸 좌표를 반환한다.

    Args:
        grid: 4x4 입력 격자.

    Returns:
        빈칸 좌표 2개를 담은 리스트.

    Raises:
        InvalidBlankCountError: 빈칸 개수가 2개가 아닌 경우.
    """
    blanks: list[tuple[int, int]] = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == BLANK_MARKER:
                blanks.append((row_idx, col_idx))

    if len(blanks) != BLANK_COUNT:
        raise InvalidBlankCountError(
            f"blank count must be {BLANK_COUNT}, got {len(blanks)}"
        )

    return blanks
