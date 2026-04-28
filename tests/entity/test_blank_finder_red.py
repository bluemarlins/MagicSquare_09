import pytest

from tests.red_helpers import DURER_MAGIC_SQUARE, copy_grid, load_attr


class TestBlankFinderRed:
    @staticmethod
    def _find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
        find_blank_coords = load_attr(
            "src.entity.services.blank_finder", "find_blank_coords"
        )
        result = find_blank_coords(grid)
        assert isinstance(result, list)
        return result

    @staticmethod
    def _invalid_blank_count_error() -> type[Exception]:
        exc = load_attr(
            "src.exceptions.domain_exceptions", "InvalidBlankCountError"
        )
        if not isinstance(exc, type) or not issubclass(exc, Exception):
            pytest.fail("RED: InvalidBlankCountError must be an Exception subclass")
        return exc

    def test_tc_ms_a_001_two_blanks_row_major(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        coords = self._find_blank_coords(matrix)

        assert coords == [(1, 3), (3, 3)]

    def test_tc_ms_a_002_diagonal_blanks_row_major(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 0
        matrix[3][3] = 0

        coords = self._find_blank_coords(matrix)

        assert coords == [(0, 0), (3, 3)]

    def test_tc_ms_a_003_raises_when_no_blank(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)

        with pytest.raises(self._invalid_blank_count_error()):
            self._find_blank_coords(matrix)

    def test_tc_ms_a_004_raises_when_one_blank(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0

        with pytest.raises(self._invalid_blank_count_error()):
            self._find_blank_coords(matrix)

    def test_tc_ms_a_005_raises_when_three_or_more_blanks(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 0
        matrix[1][1] = 0
        matrix[3][3] = 0

        with pytest.raises(self._invalid_blank_count_error()):
            self._find_blank_coords(matrix)

    def test_l_01a_first_blank_is_row_major_first(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][3] = 0
        matrix[2][1] = 0

        coords = self._find_blank_coords(matrix)

        assert len(coords) == 2
        assert coords[0] == (0, 3)

    def test_l_01b_second_blank_is_row_major_second(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][3] = 0
        matrix[2][1] = 0

        coords = self._find_blank_coords(matrix)

        assert coords[1] == (2, 1)

    def test_l_01c_optional_coordinate_range_is_one_to_four(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        coords = self._find_blank_coords(matrix)
        for row, col in coords:
            assert 1 <= row <= 4
            assert 1 <= col <= 4
