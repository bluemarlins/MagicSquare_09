from unittest.mock import MagicMock

import pytest

from tests.red_helpers import DURER_MAGIC_SQUARE, copy_grid, load_attr


class TestSolutionContractRed:
    @staticmethod
    def _solve(grid: list[list[int]]) -> list[int]:
        controller_cls = load_attr(
            "src.boundary.magic_square_controller", "MagicSquareController"
        )
        controller = controller_cls()

        if hasattr(controller, "solve"):
            response = controller.solve(grid)
        elif hasattr(controller_cls, "solve"):
            response = controller_cls.solve(grid)
        else:
            pytest.fail("RED: MagicSquareController.solve API is missing")

        if isinstance(response, dict) and "result" in response:
            return response["result"]
        if isinstance(response, list):
            return response

        pytest.fail("RED: solve response must be list or {'result': list}")

    def test_ui_05_returns_six_length_solution_array(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solve(matrix)

        assert isinstance(result, list)
        assert len(result) == 6

    def test_ui_06_returns_one_indexed_coordinates(self) -> None:
        matrix = copy_grid(DURER_MAGIC_SQUARE)
        matrix[1][3] = 0
        matrix[3][3] = 0

        result = self._solve(matrix)
        r1, c1, _, r2, c2, _ = result

        assert 1 <= r1 <= 4
        assert 1 <= c1 <= 4
        assert 1 <= r2 <= 4
        assert 1 <= c2 <= 4


class TestMagicSquareControllerDictResponse:
    """MagicSquareController가 dict 응답을 언랩하는 경로를 검증한다."""

    def test_cov_ctrl_01_solve_unwraps_dict_result_from_solver(self) -> None:
        """solver가 {'result': [...]} dict를 반환할 때 내부 list를 추출한다.

        Covers: magic_square_controller.py line 56
        """
        from src.boundary.magic_square_controller import MagicSquareController

        mock_validator = MagicMock()
        mock_validator.validate.return_value = None

        mock_solver = MagicMock()
        mock_solver.solve.return_value = {"result": [2, 4, 8, 4, 4, 1]}

        controller = MagicSquareController(
            validator=mock_validator, solver=mock_solver
        )
        result = controller.solve([[0] * 4] * 4)

        assert result == [2, 4, 8, 4, 4, 1]
