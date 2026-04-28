import pytest

from tests.red_helpers import DURER_MAGIC_SQUARE, copy_grid, load_attr


class TestMissingNumberFinderRed:
    @staticmethod
    def _find_not_exist_nums(grid: list[list[int]]) -> list[int]:
        find_not_exist_nums = load_attr(
            "src.entity.services.missing_number_finder", "find_not_exist_nums"
        )
        result = find_not_exist_nums(grid)
        assert isinstance(result, list)
        return result

    def test_l_02a_returns_two_missing_numbers(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        missing = self._find_not_exist_nums(matrix)

        assert len(missing) == 2
        assert set(missing) == {1, 8}

    def test_l_02b_returns_missing_numbers_in_ascending_order(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 0
        matrix[3][2] = 0

        missing = self._find_not_exist_nums(matrix)

        assert missing == sorted(missing)


class TestSolvingStrategyRed:
    @staticmethod
    def _solution(grid: list[list[int]]) -> list[int]:
        solution = load_attr("src.entity.services.solving_strategy", "solution")
        result = solution(grid)
        assert isinstance(result, list)
        return result

    @staticmethod
    def _no_solution_error() -> type[Exception]:
        exc = load_attr("src.exceptions.domain_exceptions", "NoSolutionError")
        if not isinstance(exc, type) or not issubclass(exc, Exception):
            pytest.fail("RED: NoSolutionError must be an Exception subclass")
        return exc

    @staticmethod
    def _invalid_blank_count_error() -> type[Exception]:
        exc = load_attr(
            "src.exceptions.domain_exceptions", "InvalidBlankCountError"
        )
        if not isinstance(exc, type) or not issubclass(exc, Exception):
            pytest.fail("RED: InvalidBlankCountError must be an Exception subclass")
        return exc

    @staticmethod
    def _apply_solution(grid: list[list[int]], result: list[int]) -> list[list[int]]:
        assert len(result) == 6
        r1, c1, n1, r2, c2, n2 = result
        completed = copy_grid(grid)
        completed[r1 - 1][c1 - 1] = n1
        completed[r2 - 1][c2 - 1] = n2
        return completed

    def test_tc_ms_c_001_returns_list_type_and_length_six(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solution(matrix)

        assert isinstance(result, list)
        assert len(result) == 6

    def test_tc_ms_c_002_returns_expected_solution_values(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solution(matrix)

        assert result == [2, 4, 8, 4, 4, 1]

    def test_tc_ms_c_003_raises_when_grid_is_already_complete(self) -> None:
        with pytest.raises(self._invalid_blank_count_error()):
            self._solution(copy_grid(DURER_MAGIC_SQUARE))

    def test_tc_ms_c_004_includes_min_value_one(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solution(matrix)

        assert 1 in (result[2], result[5])

    def test_tc_ms_c_005_includes_max_value_sixteen(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 0
        matrix[1][3] = 0

        result = self._solution(matrix)

        assert 16 in (result[2], result[5])

    def test_tc_ms_c_006_completed_grid_sums_to_thirty_four(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solution(matrix)
        completed = self._apply_solution(matrix, result)

        for row in completed:
            assert sum(row) == 34
        for col in range(4):
            assert sum(completed[row][col] for row in range(4)) == 34

    def test_tc_ms_c_007_raises_no_solution_error(self) -> None:
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 0],
            [9, 10, 11, 12],
            [13, 14, 15, 0],
        ]

        with pytest.raises(self._no_solution_error()):
            self._solution(matrix)

    def test_tc_ms_c_008_diagonal_sums_are_thirty_four(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solution(matrix)
        completed = self._apply_solution(matrix, result)

        assert completed[0][0] + completed[1][1] + completed[2][2] + completed[3][3] == 34
        assert completed[0][3] + completed[1][2] + completed[2][1] + completed[3][0] == 34

    def test_l_04a_small_missing_first_blank_strategy(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solution(matrix)

        assert result == [2, 4, 8, 4, 4, 1]

    def test_l_04b_reverse_strategy_after_first_attempt_fails(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[0][0] = 0
        matrix[3][3] = 0

        result = self._solution(matrix)
        completed = self._apply_solution(matrix, result)

        is_magic_square = load_attr(
            "src.entity.services.magic_square_validator", "is_magic_square"
        )
        assert is_magic_square(completed) is True

    def test_l_04c_solution_contract_length_and_value_set(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solution(matrix)
        missing = set(TestMissingNumberFinderRed._find_not_exist_nums(matrix))

        assert len(result) == 6
        assert 1 <= result[0] <= 4
        assert 1 <= result[1] <= 4
        assert 1 <= result[3] <= 4
        assert 1 <= result[4] <= 4
        assert {result[2], result[5]} == missing

    def test_l_04d_solution_result_forms_magic_square(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solution(matrix)
        completed = self._apply_solution(matrix, result)

        is_magic_square = load_attr(
            "src.entity.services.magic_square_validator", "is_magic_square"
        )
        assert is_magic_square(completed) is True

    def test_cov_ss_01_raises_no_solution_error_when_missing_count_not_two(
        self,
    ) -> None:
        """빈칸은 정확히 2개지만 중복 값으로 누락 숫자가 3개인 경우 NoSolutionError.

        Covers: solving_strategy.py line 26
        값 1이 중복(row 0, row 1) → 누락 집합 = {5, 15, 16} → len == 3 ≠ 2.
        blank_finder 는 빈칸 2개를 정상 처리하므로 line 26 에 도달한다.
        """
        matrix = [
            [1, 2, 3, 4],
            [1, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 0],
        ]
        with pytest.raises(self._no_solution_error()):
            self._solution(matrix)
