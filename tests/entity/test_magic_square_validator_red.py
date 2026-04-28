import pytest

from tests.red_helpers import DURER_MAGIC_SQUARE, copy_grid, load_attr


class TestMagicSquareValidatorRed:
    @staticmethod
    def _is_magic_square(grid: list[list[int]]) -> bool:
        is_magic_square = load_attr(
            "entity.services.magic_square_validator", "is_magic_square"
        )
        result = is_magic_square(grid)
        assert isinstance(result, bool)
        return result

    def test_tc_ms_b_001_returns_true_for_valid_magic_square(self) -> None:
        assert self._is_magic_square(copy_grid(DURER_MAGIC_SQUARE)) is True

    def test_tc_ms_b_002_returns_false_for_invalid_row_sum(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 17
        assert self._is_magic_square(matrix) is False

    def test_tc_ms_b_003_returns_false_for_invalid_column_sum(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 15
        assert self._is_magic_square(matrix) is False

    def test_tc_ms_b_004_returns_false_for_invalid_main_diagonal_sum(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 15
        assert self._is_magic_square(matrix) is False

    def test_tc_ms_b_005_returns_false_for_invalid_anti_diagonal_sum(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][3] = 14
        assert self._is_magic_square(matrix) is False

    def test_l_03a_returns_true_for_known_magic_square(self) -> None:
        assert self._is_magic_square(copy_grid(DURER_MAGIC_SQUARE)) is True

    def test_l_03b_returns_false_when_row_sums_mismatch(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[2][0] = 8
        assert self._is_magic_square(matrix) is False

    def test_l_03c_returns_false_when_column_sums_mismatch(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][1] = 9
        assert self._is_magic_square(matrix) is False

    def test_l_03d_returns_false_when_diagonal_sum_mismatch(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[3][3] = 2
        assert self._is_magic_square(matrix) is False

    def test_l_03e_returns_false_when_sum_is_not_34(self) -> None:
        matrix = [
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
        ]
        assert self._is_magic_square(matrix) is False
