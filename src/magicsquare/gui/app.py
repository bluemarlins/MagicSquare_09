"""PyQt6 GUI application for MagicSquare."""

from __future__ import annotations

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.boundary.magic_square_controller import MagicSquareController
from src.constants import MATRIX_SIZE


class MagicSquareWindow(QWidget):
    """MagicSquare MVP GUI window."""

    def __init__(self) -> None:
        super().__init__()
        self._controller = MagicSquareController()
        self._inputs: list[list[QLineEdit]] = []
        self._result_label = QLabel("결과: -")
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("MagicSquare 4x4 Solver")
        layout = QVBoxLayout()

        guide = QLabel("4x4 숫자를 입력하세요. 빈칸은 0으로 입력합니다.")
        guide.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(guide)

        grid_layout = QGridLayout()
        for row_idx in range(MATRIX_SIZE):
            row_widgets: list[QLineEdit] = []
            for col_idx in range(MATRIX_SIZE):
                cell = QLineEdit()
                cell.setMaxLength(2)
                cell.setFixedWidth(56)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setPlaceholderText("0")
                grid_layout.addWidget(cell, row_idx, col_idx)
                row_widgets.append(cell)
            self._inputs.append(row_widgets)
        layout.addLayout(grid_layout)

        button_layout = QHBoxLayout()
        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_click_solve)
        button_layout.addWidget(solve_button)
        layout.addLayout(button_layout)

        self._result_label.setWordWrap(True)
        layout.addWidget(self._result_label)
        self.setLayout(layout)

    def _read_grid(self) -> list[list[int]]:
        grid: list[list[int]] = []
        for row in self._inputs:
            values: list[int] = []
            for cell in row:
                text = cell.text().strip()
                raw = text if text else "0"
                values.append(int(raw))
            grid.append(values)
        return grid

    def _on_click_solve(self) -> None:
        try:
            grid = self._read_grid()
            result = self._controller.solve(grid)
            self._result_label.setText(f"결과: {result}")
        except ValueError as exc:
            QMessageBox.warning(self, "입력 오류", str(exc))
        except Exception as exc:  # pragma: no cover - unexpected runtime error
            QMessageBox.critical(self, "실행 오류", f"예상치 못한 오류: {exc}")


def run() -> int:
    """Run Qt application."""
    app = QApplication(sys.argv)
    window = MagicSquareWindow()
    window.resize(420, 320)
    window.show()
    return app.exec()
