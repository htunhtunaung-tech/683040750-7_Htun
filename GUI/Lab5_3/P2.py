"""
Htun Htun Aung
683040750-7
P2 Lab5_3
"""

import sys
import os
from collections import defaultdict
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QDoubleSpinBox,
    QMessageBox, QGroupBox, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette

try:
    import matplotlib
    matplotlib.use("QtAgg")
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.patches as mpatches
    import numpy as np
except ImportError:
    print("Please install matplotlib: pip install matplotlib")
    sys.exit(1)


# ── Palette constants (also used by matplotlib canvas) ───────────────────────
BG_DARK   = "#0f1117"
BG_PANEL  = "#1a1d27"
BG_INPUT  = "#252837"
ACCENT    = "#6c63ff"
ACCENT2   = "#ff6584"
TEXT_PRI  = "#e8e8f0"
TEXT_SEC  = "#9494a8"
BORDER    = "#2e3147"

CATEGORY_COLORS = {
    "Electronics": "#6c63ff",
    "Clothing":    "#ff6584",
    "Food":        "#43d9ad",
    "Others":      "#ffb347",
}

MONTHS_ORDER = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]


# ── Stylesheet loader ─────────────────────────────────────────────────────────
def load_stylesheet(qss_path: str = "style.qss") -> str:
    """Load QSS from an external file. Falls back to empty string on error."""
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[Warning] Stylesheet not found: {qss_path}")
        return ""
    except Exception as e:
        print(f"[Warning] Could not load stylesheet: {e}")
        return ""


# ── Canvas ────────────────────────────────────────────────────────────────────
class SalesCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 5), facecolor=BG_PANEL)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ax = self.fig.add_subplot(111)
        self._style_axes()
        self.draw()

    def _style_axes(self):
        ax = self.ax
        ax.set_facecolor(BG_DARK)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor(BORDER)
        ax.yaxis.grid(True, color=BORDER, linewidth=0.6, linestyle="--")
        ax.set_axisbelow(True)
        ax.set_title("Monthly Sales by Category", color=TEXT_PRI,
                     fontsize=13, fontweight="bold", pad=14,
                     fontfamily="monospace")
        ax.set_xlabel("Month", color=TEXT_SEC, fontsize=10)
        ax.set_ylabel("Sales Amount ($)", color=TEXT_SEC, fontsize=10)
        self.fig.tight_layout(pad=2.2)

    def refresh(self, data: dict):
        """data: {category: {month: amount}}"""
        self.ax.clear()
        self._style_axes()

        months_present = [m for m in MONTHS_ORDER
                          if any(m in data[c] for c in data)]
        if not months_present:
            self.ax.text(0.5, 0.5, "No data yet – add some sales!",
                         ha="center", va="center", color=TEXT_SEC,
                         fontsize=11, transform=self.ax.transAxes)
            self.draw()
            return

        n_cats = len(data)
        n_months = len(months_present)
        width = 0.7 / max(n_cats, 1)
        x = np.arange(n_months)
        offsets = np.linspace(-(n_cats - 1) / 2, (n_cats - 1) / 2, n_cats) * width

        patches = []
        for i, (cat, monthly) in enumerate(data.items()):
            values = [monthly.get(m, 0) for m in months_present]
            bars = self.ax.bar(
                x + offsets[i], values, width=width * 0.88,
                color=CATEGORY_COLORS.get(cat, "#aaaaaa"),
                zorder=3, alpha=0.92,
                label=cat
            )
            for bar, val in zip(bars, values):
                if val > 0:
                    self.ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + max(values) * 0.01,
                        f"${val:,.0f}",
                        ha="center", va="bottom",
                        color=TEXT_SEC, fontsize=7.5, fontfamily="monospace"
                    )
            patches.append(mpatches.Patch(
                facecolor=CATEGORY_COLORS.get(cat, "#aaaaaa"), label=cat))

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(months_present, color=TEXT_SEC)
        self.ax.tick_params(axis="x", colors=TEXT_SEC)
        self.ax.tick_params(axis="y", colors=TEXT_SEC)

        self.ax.legend(
            handles=patches, loc="upper left",
            facecolor=BG_PANEL, edgecolor=BORDER,
            labelcolor=TEXT_PRI, fontsize=9,
            framealpha=0.9
        )

        self.fig.tight_layout(pad=2.2)
        self.draw()


# ── Main Window ───────────────────────────────────────────────────────────────
class SalesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Chart")
        self.resize(1100, 700)
        self.setMinimumSize(850, 560)

        # data store: {category: {month: total_amount}}
        self.sales_data: dict = defaultdict(lambda: defaultdict(float))

        self._build_ui()

    # ── Build UI ───────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)

        # ── Left panel ──────────────────────────────────────────────────
        left = QWidget()
        left.setFixedWidth(270)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        # Header (inline style kept — references runtime color constants)
        header = QLabel("SALES\nTRACKER")
        header.setStyleSheet(f"""
            font-size: 24px; font-weight: 900; color: {TEXT_PRI};
            letter-spacing: 3px; line-height: 1.1;
        """)
        left_layout.addWidget(header)

        sub = QLabel("Monthly performance dashboard")
        sub.setStyleSheet(f"color: {TEXT_SEC}; font-size: 10px; margin-bottom:6px;")
        left_layout.addWidget(sub)

        div = QFrame()
        div.setObjectName("divider")
        left_layout.addWidget(div)

        # ── Import group ─────────────────────────────────────────────────
        grp_import = QGroupBox("IMPORT FILE")
        gi = QVBoxLayout(grp_import)
        gi.setSpacing(6)

        self.filename_edit = QLineEdit()
        self.filename_edit.setPlaceholderText("e.g. sales_data.txt")
        gi.addWidget(QLabel("Filename"))
        gi.addWidget(self.filename_edit)

        self.file_status = QLabel("")
        self.file_status.setStyleSheet("font-size: 10px; color: #43d9ad;")
        gi.addWidget(self.file_status)

        btn_import = QPushButton("⬆  Import Data")
        btn_import.setObjectName("btn_import")
        btn_import.clicked.connect(self._import_data)
        gi.addWidget(btn_import)

        left_layout.addWidget(grp_import)

        # ── Add data group ────────────────────────────────────────────────
        grp_add = QGroupBox("ADD ENTRY")
        ga = QVBoxLayout(grp_add)
        ga.setSpacing(6)

        ga.addWidget(QLabel("Month"))
        self.month_combo = QComboBox()
        self.month_combo.addItems(MONTHS_ORDER)
        ga.addWidget(self.month_combo)

        ga.addWidget(QLabel("Sales Amount ($)"))
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0, 10_000_000)
        self.amount_spin.setDecimals(2)
        self.amount_spin.setSingleStep(100)
        self.amount_spin.setGroupSeparatorShown(True)
        ga.addWidget(self.amount_spin)

        ga.addWidget(QLabel("Product Category"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(["Electronics", "Clothing", "Food", "Others"])
        ga.addWidget(self.cat_combo)

        btn_add = QPushButton("＋  Add Data")
        btn_add.setObjectName("btn_add")
        btn_add.clicked.connect(self._add_data)
        ga.addWidget(btn_add)

        left_layout.addWidget(grp_add)

        # ── Clear button ──────────────────────────────────────────────────
        btn_clear = QPushButton("✕  Clear Chart")
        btn_clear.setObjectName("btn_clear")
        btn_clear.clicked.connect(self._clear_data)
        left_layout.addWidget(btn_clear)

        left_layout.addStretch()

        # ── Status label ──────────────────────────────────────────────────
        self.status_label = QLabel("Ready.")
        self.status_label.setStyleSheet(f"color:{TEXT_SEC}; font-size:10px;")
        left_layout.addWidget(self.status_label)

        root.addWidget(left)

        # ── Right panel (chart) ───────────────────────────────────────────
        right = QWidget()
        right.setStyleSheet(f"background-color:{BG_PANEL}; border-radius:10px;")
        rl = QVBoxLayout(right)
        rl.setContentsMargins(8, 8, 8, 8)

        self.canvas = SalesCanvas(right)
        rl.addWidget(self.canvas)

        root.addWidget(right, stretch=1)

    # ── Slots ──────────────────────────────────────────────────────────────
    def _add_data(self):
        month = self.month_combo.currentText()
        amount = self.amount_spin.value()
        cat = self.cat_combo.currentText()

        if amount <= 0:
            self._set_status("⚠ Sales amount must be greater than 0.", error=True)
            return

        self.sales_data[cat][month] += amount
        self._set_status(f"✓ Added ${amount:,.2f} for {cat} in {month}.")
        self.canvas.refresh(self.sales_data)

    def _clear_data(self):
        reply = QMessageBox.question(
            self, "Clear Chart",
            "Are you sure you want to clear all sales data?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.sales_data.clear()
            self.canvas.refresh(self.sales_data)
            self._set_status("Chart cleared.")

    def _import_data(self):
        """
        Import sales data from a text file.
        Expected format (one entry per line):
            Month,Category,Amount
        e.g.:
            Jan,Electronics,1500.00
            Feb,Clothing,800
        """
        path = self.filename_edit.text().strip()
        if not path:
            self._set_status("⚠ Please enter a filename.", error=True)
            self.file_status.setText("")
            return

        if not os.path.exists(path):
            self._set_status(f"⚠ File not found: {path}", error=True)
            self.file_status.setStyleSheet("font-size:10px; color:#ff6584;")
            self.file_status.setText("✗ File does not exist")
            return

        self.file_status.setStyleSheet("font-size:10px; color:#43d9ad;")
        self.file_status.setText("✓ File found")

        errors = []
        count = 0
        try:
            with open(path, "r") as f:
                for lineno, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) != 3:
                        errors.append(f"Line {lineno}: expected 3 fields, got {len(parts)}")
                        continue
                    month, cat, amt_str = parts
                    if month not in MONTHS_ORDER:
                        errors.append(f"Line {lineno}: unknown month '{month}'")
                        continue
                    if cat not in CATEGORY_COLORS:
                        errors.append(f"Line {lineno}: unknown category '{cat}'")
                        continue
                    try:
                        amount = float(amt_str)
                    except ValueError:
                        errors.append(f"Line {lineno}: invalid amount '{amt_str}'")
                        continue
                    self.sales_data[cat][month] += amount
                    count += 1
        except Exception as e:
            self._set_status(f"⚠ Error reading file: {e}", error=True)
            return

        self.canvas.refresh(self.sales_data)

        if errors:
            detail = "\n".join(errors[:10])
            if len(errors) > 10:
                detail += f"\n…and {len(errors)-10} more."
            QMessageBox.warning(self, "Import Warnings",
                                f"Imported {count} records with {len(errors)} error(s):\n\n{detail}")
            self._set_status(f"Imported {count} records ({len(errors)} skipped).")
        else:
            self._set_status(f"✓ Imported {count} records from '{path}'.")

    def _set_status(self, msg: str, error: bool = False):
        color = ACCENT2 if error else "#43d9ad"
        self.status_label.setStyleSheet(f"color:{color}; font-size:10px;")
        self.status_label.setText(msg)


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Load QSS from the same directory as this script
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    app.setStyleSheet(load_stylesheet(qss_path))

    # Dark palette baseline so native widgets inherit dark colours
    palette = QPalette()
    palette.setColor(QPalette.Window,      QColor(BG_DARK))
    palette.setColor(QPalette.WindowText,  QColor(TEXT_PRI))
    palette.setColor(QPalette.Base,        QColor(BG_INPUT))
    palette.setColor(QPalette.Text,        QColor(TEXT_PRI))
    palette.setColor(QPalette.Button,      QColor(BG_PANEL))
    palette.setColor(QPalette.ButtonText,  QColor(TEXT_PRI))
    palette.setColor(QPalette.Highlight,   QColor(ACCENT))
    app.setPalette(palette)

    window = SalesApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()