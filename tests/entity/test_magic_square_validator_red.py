import pytest

from tests.red_helpers import DURER_MAGIC_SQUARE, copy_grid, load_attr


class TestMagicSquareValidatorRed:
    @staticmethod
    def _is_magic_square(grid: list[list[int]]) -> bool:
        is_magic_square = load_attr(
            "src.entity.services.magic_square_validator", "is_magic_square"
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

    def test_cov_mv_01_returns_false_for_grid_with_three_rows(self) -> None:
        """행이 3개인 격자는 False를 반환한다.

        Covers: magic_square_validator.py line 16 (len(grid) != GRID_SIZE 분기)
        """
        matrix = [
            [16, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
        ]
        assert self._is_magic_square(matrix) is False

    def test_cov_mv_02_returns_false_for_jagged_row(self) -> None:
        """열 수가 4가 아닌 행이 포함된 격자는 False를 반환한다.

        Covers: magic_square_validator.py line 18 (len(row) != GRID_SIZE 분기)
        """
        matrix = [
            [16, 3, 2, 13],
            [5, 10, 11],
            [9, 6, 7, 12],
            [4, 15, 14, 1],
        ]
        assert self._is_magic_square(matrix) is False

    def test_cov_mv_03_returns_false_when_only_column_sum_fails(self) -> None:
        """행 합과 값 집합은 유효하지만 열 합이 틀린 격자는 False를 반환한다.

        Covers: magic_square_validator.py line 31 (열 합 불일치 분기)
        뒤러 마방진 0행의 첫째·넷째 값을 교환하면 행 합(34)은 유지되나
        0열 합(13+5+9+4=31)이 34가 되지 않는다.
        """
        matrix = [
            [13, 3, 2, 16],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 1],
        ]
        assert self._is_magic_square(matrix) is False
