"""MagicSquare boundary controller.

UI(Boundary)는 로직을 직접 판단하지 않고 주입받은 validator/solver에 위임한다.
"""

from __future__ import annotations

from typing import Callable, Protocol

from src.boundary.input_validator import InputValidator
from src.entity.services.solving_strategy import solution as solve_magic_square


class _SolverProtocol(Protocol):
    def solve(self, grid: list[list[int]]) -> list[int] | dict[str, list[int]]:
        """입력 격자를 받아 결과를 반환한다."""


class _FunctionSolver:
    """함수 기반 solver 어댑터.

    Domain 함수를 주입받아 Protocol 형태로 맞춘다.
    """

    def __init__(self, solve_func: Callable[[list[list[int]]], list[int]]) -> None:
        self._solve_func = solve_func

    def solve(self, grid: list[list[int]]) -> list[int]:
        return self._solve_func(grid)


class MagicSquareController:
    """Boundary 진입점.

    주입받은 solver를 호출하고, 응답 계약(list[int] 길이 6)을 맞춘다.
    """

    def __init__(
        self, validator: InputValidator | None = None, solver: _SolverProtocol | None = None
    ) -> None:
        self._validator = validator or InputValidator()
        self._solver: _SolverProtocol = solver or _FunctionSolver(solve_magic_square)

    def solve(self, grid: list[list[int]]) -> list[int]:
        """주입된 solver로 문제를 해결한다.

        Args:
            grid: 4x4 입력 격자.

        Returns:
            [r1, c1, n1, r2, c2, n2] 형식의 정수 리스트.
        """
        self._validator.validate(grid)
        response = self._solver.solve(grid)
        if isinstance(response, dict) and "result" in response:
            return response["result"]
        return response
