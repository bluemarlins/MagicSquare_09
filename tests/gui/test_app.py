"""GUI app 테스트 — coverage 보강용.

PyQt6 없이 실행 가능하도록 sys.modules에 스텁 모듈을 등록한 뒤
실제 소스를 import 한다.
"""

from __future__ import annotations

import sys
from types import ModuleType
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# PyQt6 스텁 등록
# ---------------------------------------------------------------------------

def _register_pyqt6_stubs() -> None:
    """Qt 없이 테스트할 수 있도록 최소한의 스텁을 sys.modules에 주입한다."""
    if "PyQt6" in sys.modules:
        return

    class _Widget:
        def __init__(self) -> None:
            pass

        def setWindowTitle(self, t: str) -> None:
            pass

        def setLayout(self, l: object) -> None:
            pass

        def resize(self, w: int, h: int) -> None:
            pass

        def show(self) -> None:
            pass

    class _Label(_Widget):
        def __init__(self, text: str = "") -> None:
            self._text = text

        def setAlignment(self, flag: object) -> None:
            pass

        def setWordWrap(self, v: bool) -> None:
            pass

        def setText(self, text: str) -> None:
            self._text = text

    class _LineEdit(_Widget):
        def __init__(self) -> None:
            self._text = ""

        def setMaxLength(self, n: int) -> None:
            pass

        def setFixedWidth(self, n: int) -> None:
            pass

        def setAlignment(self, flag: object) -> None:
            pass

        def setPlaceholderText(self, t: str) -> None:
            pass

        def text(self) -> str:
            return self._text

    class _PushButton(_Widget):
        def __init__(self, label: str = "") -> None:
            self._clicked_signal: MagicMock = MagicMock()

        @property
        def clicked(self) -> MagicMock:
            return self._clicked_signal

    class _Layout:
        def addWidget(self, *args: object) -> None:
            pass

        def addLayout(self, *args: object) -> None:
            pass

    class _Application:
        def __init__(self, args: list) -> None:
            pass

        def exec(self) -> int:
            return 0

    _qwidgets = ModuleType("PyQt6.QtWidgets")
    _qwidgets.QWidget = _Widget           # type: ignore[attr-defined]
    _qwidgets.QLabel = _Label             # type: ignore[attr-defined]
    _qwidgets.QLineEdit = _LineEdit       # type: ignore[attr-defined]
    _qwidgets.QPushButton = _PushButton   # type: ignore[attr-defined]
    _qwidgets.QVBoxLayout = _Layout       # type: ignore[attr-defined]
    _qwidgets.QHBoxLayout = _Layout       # type: ignore[attr-defined]
    _qwidgets.QGridLayout = _Layout       # type: ignore[attr-defined]
    _qwidgets.QMessageBox = MagicMock()   # type: ignore[attr-defined]
    _qwidgets.QApplication = _Application # type: ignore[attr-defined]

    _qcore = ModuleType("PyQt6.QtCore")
    _qcore.Qt = MagicMock()              # type: ignore[attr-defined]

    _pyqt6 = ModuleType("PyQt6")

    sys.modules["PyQt6"] = _pyqt6
    sys.modules["PyQt6.QtCore"] = _qcore
    sys.modules["PyQt6.QtWidgets"] = _qwidgets


_register_pyqt6_stubs()

# 스텁 등록 이후 import — 순서 중요
from src.magicsquare.gui.app import MagicSquareWindow, run  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers / Fixtures
# ---------------------------------------------------------------------------

def _qmessagebox() -> MagicMock:
    """app.py가 바인딩한 QMessageBox 스텁 인스턴스를 반환한다."""
    return sys.modules["PyQt6.QtWidgets"].QMessageBox  # type: ignore[return-value]


@pytest.fixture()
def window() -> MagicSquareWindow:
    """매 테스트마다 새 MagicSquareWindow를 생성하고 controller를 Mock으로 교체한다."""
    w = MagicSquareWindow()
    w._controller = MagicMock()
    return w


@pytest.fixture(autouse=True)
def _reset_qmessagebox() -> None:
    """각 테스트 전 QMessageBox mock 상태를 초기화한다."""
    _qmessagebox().reset_mock()


# ---------------------------------------------------------------------------
# TestReadGrid — _read_grid() 메서드
# ---------------------------------------------------------------------------

class TestReadGrid:
    """_read_grid()가 위젯 텍스트를 int 격자로 변환하는지 검증한다."""

    def test_cov_gui_01_read_grid_converts_text_to_int(self) -> None:
        """입력 텍스트를 정수로 변환한다."""
        w = MagicSquareWindow()
        w._inputs[0][0]._text = "16"
        w._inputs[0][3]._text = "13"

        grid = w._read_grid()

        assert grid[0][0] == 16
        assert grid[0][3] == 13

    def test_cov_gui_02_read_grid_treats_empty_text_as_zero(self) -> None:
        """빈 문자열 셀은 0으로 변환한다."""
        w = MagicSquareWindow()
        w._inputs[2][1]._text = ""

        grid = w._read_grid()

        assert grid[2][1] == 0

    def test_cov_gui_03_read_grid_returns_4x4_shape(self) -> None:
        """반환된 격자가 4×4 형태인지 확인한다."""
        w = MagicSquareWindow()

        grid = w._read_grid()

        assert len(grid) == 4
        assert all(len(row) == 4 for row in grid)


# ---------------------------------------------------------------------------
# TestOnClickSolve — _on_click_solve() 메서드
# ---------------------------------------------------------------------------

class TestOnClickSolve:
    """_on_click_solve() 의 성공 / 예외 경로를 검증한다."""

    def test_cov_gui_04_updates_result_label_on_success(
        self, window: MagicSquareWindow
    ) -> None:
        """풀기 성공 시 결과 레이블을 업데이트한다."""
        expected = [2, 4, 8, 4, 4, 1]
        window._controller.solve.return_value = expected

        window._on_click_solve()

        assert window._result_label._text == f"결과: {expected}"

    def test_cov_gui_05_calls_warning_on_value_error(
        self, window: MagicSquareWindow
    ) -> None:
        """ValueError 발생 시 QMessageBox.warning을 호출한다."""
        window._controller.solve.side_effect = ValueError("잘못된 입력")

        window._on_click_solve()

        _qmessagebox().warning.assert_called_once()


# ---------------------------------------------------------------------------
# TestRun — run() 함수
# ---------------------------------------------------------------------------

class TestRun:
    def test_cov_gui_06_run_returns_zero(self) -> None:
        """run()이 정수 0을 반환한다 (stub exec() → 0)."""
        result = run()

        assert isinstance(result, int)
        assert result == 0


# ---------------------------------------------------------------------------
# Test __main__.py entrypoint
# ---------------------------------------------------------------------------

class TestMainEntrypoint:
    def test_cov_main_01_entrypoint_raises_system_exit(self) -> None:
        """__main__.py 실행 시 run()을 호출하고 SystemExit을 발생시킨다."""
        import runpy
        import src.magicsquare.gui.app as _app_module

        sys.modules.pop("src.magicsquare.gui.__main__", None)

        with patch.object(_app_module, "run", return_value=42):
            with pytest.raises(SystemExit) as exc_info:
                runpy.run_module(
                    "src.magicsquare.gui.__main__",
                    run_name="__main__",
                )

        assert exc_info.value.code == 42
