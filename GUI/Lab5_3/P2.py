"""Htun Htun Aung
683040750-7
Lab5_3 P2
"""

import sys
import os
from collections import defaultdict

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QGroupBox,
    QMessageBox, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
CATEGORIES = ["Electronics", "Clothing", "Food", "Others"]
COLORS = {
    "Electronics": "#7EB8E8",
    "Clothing":    "#F4A47A",
    "Food":        "#8FD4A8",
    "Others":      "#C9A8E0",
}


class SalesChart(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(8, 5), tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def update_chart(self, data):
        self.ax.clear()

        x = np.arange(len(MONTHS))
        n_cats = len(CATEGORIES)
        width = 0.2
        offsets = np.linspace(-(n_cats - 1) / 2, (n_cats - 1) / 2, n_cats) * width

        has_data = False
        for i, cat in enumerate(CATEGORIES):
            values = [data[month].get(cat, 0) for month in MONTHS]
            if any(v > 0 for v in values):
                has_data = True
            bars = self.ax.bar(
                x + offsets[i], values, width,
                label=cat, color=COLORS[cat], alpha=0.85
            )
            # Add value labels on bars
            for bar, val in zip(bars, values):
                if val > 0:
                    self.ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + bar.get_height() * 0.01,
                        f"{val/1000:.1f}k" if val >= 1000 else str(val),
                        ha="center", va="bottom", fontsize=6.5, color="#333"
                    )

        self.ax.set_title("Monthly Sales by Product Category", fontsize=13, fontweight="bold", pad=10)
        self.ax.set_xlabel("Month", fontsize=10)
        self.ax.set_ylabel("Sales Amount ($)", fontsize=10)
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(MONTHS)
        self.ax.legend(loc="upper left", fontsize=9)
        self.ax.yaxis.grid(True, linestyle="--", alpha=0.5)
        self.ax.set_axisbelow(True)
        self.fig.patch.set_facecolor("#F9F9F9")
        self.ax.set_facecolor("#F9F9F9")

        self.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Data Chart")
        self.resize(1000, 620)
        self.data = {month: {} for month in MONTHS}

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- Left panel ---
        left = QWidget()
        left.setFixedWidth(240)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        # Import group
        import_group = QGroupBox("Import Data")
        import_layout = QVBoxLayout(import_group)
        self.filename_input = QLineEdit("sales_data.txt")
        self.filename_input.setPlaceholderText("Filename...")
        import_layout.addWidget(self.filename_input)
        import_btn = QPushButton("📁  Import Data")
        import_btn.clicked.connect(self.import_data)
        import_layout.addWidget(import_btn)
        left_layout.addWidget(import_group)

        # Add data group
        add_group = QGroupBox("Add Data")
        add_layout = QVBoxLayout(add_group)

        add_layout.addWidget(QLabel("Month"))
        self.month_combo = QComboBox()
        self.month_combo.addItems(MONTHS)
        add_layout.addWidget(self.month_combo)

        add_layout.addWidget(QLabel("Sales Amount ($)"))
        self.amount_spin = QSpinBox()
        self.amount_spin.setRange(0, 10_000_000)
        self.amount_spin.setValue(10000)
        self.amount_spin.setSingleStep(500)
        add_layout.addWidget(self.amount_spin)

        add_layout.addWidget(QLabel("Product Category"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(CATEGORIES)
        add_layout.addWidget(self.cat_combo)

        add_btn = QPushButton("＋  Add Data")
        add_btn.clicked.connect(self.add_data)
        add_layout.addWidget(add_btn)
        left_layout.addWidget(add_group)

        # Clear button
        clear_btn = QPushButton("✕  Clear Chart")
        clear_btn.clicked.connect(self.clear_chart)
        left_layout.addWidget(clear_btn)

        left_layout.addStretch()
        main_layout.addWidget(left)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # --- Chart ---
        self.chart = SalesChart()
        main_layout.addWidget(self.chart, stretch=1)
        self.chart.update_chart(self.data)

    def import_data(self):
        filename = self.filename_input.text().strip()
        if not os.path.exists(filename):
            QMessageBox.warning(self, "File Not Found", f"File '{filename}' does not exist.")
            return

        try:
            with open(filename, "r") as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) != 3:
                        QMessageBox.warning(self, "Parse Error",
                            f"Line {line_no}: expected 'Month, Amount, Category' — got: {line}")
                        return
                    month, amount_str, cat = parts
                    if month not in MONTHS:
                        QMessageBox.warning(self, "Parse Error",
                            f"Line {line_no}: unknown month '{month}'.")
                        return
                    if cat not in CATEGORIES:
                        QMessageBox.warning(self, "Parse Error",
                            f"Line {line_no}: unknown category '{cat}'.")
                        return
                    amount = float(amount_str)
                    self.data[month][cat] = self.data[month].get(cat, 0) + amount

            self.chart.update_chart(self.data)
            QMessageBox.information(self, "Success", f"Data imported from '{filename}'.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_data(self):
        month = self.month_combo.currentText()
        amount = self.amount_spin.value()
        cat = self.cat_combo.currentText()
        self.data[month][cat] = self.data[month].get(cat, 0) + amount
        self.chart.update_chart(self.data)

    def clear_chart(self):
        self.data = {month: {} for month in MONTHS}
        self.chart.update_chart(self.data)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()