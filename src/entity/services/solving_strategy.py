"""두 빈칸 마방진 해결 전략."""

from itertools import permutations

from src.entity.services.blank_finder import find_blank_coords
from src.entity.services.magic_square_validator import is_magic_square
from src.entity.services.missing_number_finder import find_not_exist_nums
from src.exceptions.domain_exceptions import NoSolutionError


def solution(grid: list[list[int]]) -> list[int]:
    """두 빈칸을 채워 마방진 해를 반환한다.

    Args:
        grid: 4x4 입력 격자.

    Returns:
        [r1, c1, n1, r2, c2, n2] 형식의 1-index 결과.

    Raises:
        NoSolutionError: 유효한 해를 찾지 못한 경우.
    """
    blanks = find_blank_coords(grid)
    missing = find_not_exist_nums(grid)
    if len(missing) != 2:
        raise NoSolutionError("missing number count must be 2")

    (r1, c1), (r2, c2) = blanks
    preferred_order = [tuple(sorted(missing, reverse=True)), tuple(sorted(missing))]

    tried: set[tuple[int, int]] = set()
    for n1, n2 in preferred_order + list(permutations(missing, 2)):
        if (n1, n2) in tried:
            continue
        tried.add((n1, n2))

        candidate = [row[:] for row in grid]
        candidate[r1][c1] = n1
        candidate[r2][c2] = n2
        if is_magic_square(candidate):
            return [r1 + 1, c1 + 1, n1, r2 + 1, c2 + 1, n2]

    raise NoSolutionError("no valid solution for given grid")
