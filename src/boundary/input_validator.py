"""Boundary 입력 검증기."""

from src.constants import BLANK_COUNT, BLANK_MARKER, MATRIX_SIZE


class InputValidator:
    """Boundary 계층 입력 검증."""

    def validate(self, grid: list[list[int]] | None) -> bool:
        """입력 격자 기본 형태를 검증한다.

        Args:
            grid: 검증 대상 격자.

        Returns:
            유효한 경우 True.

        Raises:
            ValueError: 입력이 MATRIX_SIZE x MATRIX_SIZE 형태가 아닌 경우.
        """
        if grid is None:
            raise ValueError("grid must not be None")

        if len(grid) != MATRIX_SIZE:
            raise ValueError("grid row count is invalid")

        for row in grid:
            if len(row) != MATRIX_SIZE:
                raise ValueError("grid column count is invalid")

        blank_count = 0
        non_zero_values: set[int] = set()
        max_value = MATRIX_SIZE * MATRIX_SIZE
        for row in grid:
            for value in row:
                if not isinstance(value, int):
                    raise ValueError("grid value type is invalid")
                if value == BLANK_MARKER:
                    blank_count += 1
                    continue
                if value < 1 or value > max_value:
                    raise ValueError("grid value range is invalid")
                if value in non_zero_values:
                    raise ValueError("duplicate non-zero value is invalid")
                non_zero_values.add(value)

        if blank_count != BLANK_COUNT:
            raise ValueError("blank count is invalid")

        return True
