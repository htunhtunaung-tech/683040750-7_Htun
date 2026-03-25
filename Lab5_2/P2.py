"""
Htun Htun Aung
683040750-7
P2 Lab5_2
"""

import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QGridLayout, QPushButton, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(320, 480)
        self.expression = ""

        self.setStyleSheet("background-color: #f0f0f0;")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        # Title
        title = QLabel("Standard")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title.setStyleSheet("color: #333;")
        main_layout.addWidget(title)

        # Display
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setFont(QFont("Segoe UI", 32))
        self.display.setMinimumHeight(80)
        self.display.setStyleSheet("color: #111; padding-right: 8px;")
        main_layout.addWidget(self.display)

        # Button grid
        grid = QGridLayout()
        grid.setSpacing(6)
        main_layout.addLayout(grid)

        buttons = [
            ("%",   0, 0), ("CE",     0, 1), ("C",       0, 2), ("<-",  0, 3),
            ("1/x", 1, 0), ("x^2",   1, 1), ("sqrt(x)", 1, 2), ("/",   1, 3),
            ("7",   2, 0), ("8",      2, 1), ("9",       2, 2), ("x",   2, 3),
            ("4",   3, 0), ("5",      3, 1), ("6",       3, 2), ("-",   3, 3),
            ("1",   4, 0), ("2",      4, 1), ("3",       4, 2), ("+",   4, 3),
            ("+/-", 5, 0), ("0",      5, 1), (".",       5, 2), ("=",   5, 3),
        ]

        special = {"%", "CE", "C", "<-", "1/x", "x^2", "sqrt(x)",
                   "/", "x", "-", "+"}

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setFont(QFont("Segoe UI", 12))
            btn.setMinimumHeight(52)

            if text == "=":
                style = (
                    "QPushButton { background-color: #0078d4; color: white; "
                    "border-radius: 4px; }"
                    "QPushButton:hover { background-color: #005fa3; }"
                    "QPushButton:pressed { background-color: #004a80; }"
                )
            elif text in {"C", "CE", "<-"}:
                style = (
                    "QPushButton { background-color: #e8e8e8; color: #111111; "
                    "border-radius: 4px; }"
                    "QPushButton:hover { background-color: #d0d0d0; }"
                    "QPushButton:pressed { background-color: #b8b8b8; }"
                )
            elif text in special:
                style = (
                    "QPushButton { background-color: #e0e0e0; color: #333; "
                    "border-radius: 4px; }"
                    "QPushButton:hover { background-color: #c8c8c8; }"
                    "QPushButton:pressed { background-color: #b0b0b0; }"
                )
            else:
                style = (
                    "QPushButton { background-color: #ffffff; color: #111; "
                    "border-radius: 4px; border: 1px solid #ddd; }"
                    "QPushButton:hover { background-color: #f0f0f0; }"
                    "QPushButton:pressed { background-color: #e0e0e0; }"
                )

            btn.setStyleSheet(style)
            btn.clicked.connect(lambda checked, t=text: self.on_button(t))
            grid.addWidget(btn, row, col)

    def update_display(self):
        self.display.setText(self.expression if self.expression else "0")

    def on_button(self, text):
        if text == "C":
            self.expression = ""
        elif text == "CE":
            self.expression = ""
        elif text == "<-":
            self.expression = self.expression[:-1]
        elif text == "=":
            try:
                # Replace display operators with Python operators
                expr = self.expression.replace("x", "*").replace("%", "%")
                result = eval(expr)
                # Clean up result
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)
            except Exception:
                self.expression = "Error"
        elif text == "1/x":
            try:
                val = float(eval(self.expression.replace("x", "*")))
                result = 1 / val
                self.expression = str(int(result) if isinstance(result, float) and result.is_integer() else result)
            except Exception:
                self.expression = "Error"
        elif text == "x^2":
            try:
                val = float(eval(self.expression.replace("x", "*")))
                result = val ** 2
                self.expression = str(int(result) if isinstance(result, float) and result.is_integer() else result)
            except Exception:
                self.expression = "Error"
        elif text == "sqrt(x)":
            try:
                val = float(eval(self.expression.replace("x", "*")))
                result = math.sqrt(val)
                self.expression = str(result)
            except Exception:
                self.expression = "Error"
        elif text == "+/-":
            try:
                val = float(eval(self.expression.replace("x", "*")))
                val = -val
                self.expression = str(int(val) if val == int(val) else val)
            except Exception:
                self.expression = "Error"
        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += text

        self.update_display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())