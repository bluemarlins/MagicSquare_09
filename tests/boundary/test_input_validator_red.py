import pytest

from tests.red_helpers import DURER_MAGIC_SQUARE, copy_grid, load_attr


class TestInputValidatorRed:
    @staticmethod
    def _validate(grid: list[list[int]] | None) -> object:
        validator_cls = load_attr("boundary.input_validator", "InputValidator")
        validator = validator_cls()

        if hasattr(validator, "validate"):
            return validator.validate(grid)
        if hasattr(validator_cls, "validate"):
            return validator_cls.validate(grid)

        pytest.fail("RED: InputValidator.validate API is missing")

    def test_tc_ms_d_001_invalid_cell_value_over_16(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 17

        with pytest.raises(Exception):
            self._validate(matrix)

    def test_tc_ms_d_002_invalid_grid_size_five_columns(self) -> None:
        matrix = [
            [16, 3, 2, 13, 99],
            [5, 10, 11, 8, 99],
            [9, 6, 7, 12, 99],
            [4, 15, 14, 1, 99],
        ]
        with pytest.raises(Exception):
            self._validate(matrix)

    def test_tc_ms_d_003_invalid_grid_size_three_by_three(self) -> None:
        matrix = [
            [8, 1, 6],
            [3, 5, 7],
            [4, 9, 2],
        ]
        with pytest.raises(Exception):
            self._validate(matrix)

    def test_tc_ms_d_004_invalid_input_none(self) -> None:
        with pytest.raises(Exception):
            self._validate(None)

    def test_tc_ms_d_005_invalid_string_cell_value(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[2][2] = "A"  # type: ignore[assignment]

        with pytest.raises(Exception):
            self._validate(matrix)

    def test_tc_ms_d_006_invalid_jagged_grid(self) -> None:
        matrix = [
            [16, 3, 2, 13],
            [5, 10, 11],
            [9, 6, 7, 12],
            [4, 15, 14, 1],
        ]
        with pytest.raises(Exception):
            self._validate(matrix)

    def test_ui_01_rejects_non_4x4_shape(self) -> None:
        matrix = [[1, 2, 3, 4]] * 3
        with pytest.raises(Exception):
            self._validate(matrix)

    def test_ui_02_rejects_invalid_blank_count(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 0
        with pytest.raises(Exception):
            self._validate(matrix)

    def test_ui_03_rejects_out_of_range_values(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[3][3] = 99
        with pytest.raises(Exception):
            self._validate(matrix)

    def test_ui_04_rejects_duplicate_non_zero_values(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[3][3] = 16
        with pytest.raises(Exception):
            self._validate(matrix)
