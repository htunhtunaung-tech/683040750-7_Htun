"""
Htun Htun Aung
683040750-7
P1 Lab5_3
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QComboBox, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont, QIcon


def load_students(filepath: str) -> dict[str, str]:
    """Read students.txt and return {student_id: name} dict."""
    students = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "," in line:
                    sid, name = line.split(",", 1)
                    students[sid.strip()] = name.strip()
    except FileNotFoundError:
        print(f"Warning: '{filepath}' not found. No students loaded.")
    return students

def load_stylesheet(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("styles.qss not found!")
        return ""


def compute_grade(average: float) -> str:
    if average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"

# Grade → row background color
GRADE_COLORS = {
    "A": ("#1e1e2e", "#a6e3a1"),   # (default bg, grade cell bg)
    "B": ("#1e1e2e", "#89b4fa"),
    "C": ("#1e1e2e", "#cba6f7"),
    "D": ("#1e1e2e", "#f9e2af"),
    "F": ("#f38ba8", "#f38ba8"),   # full row red for F
}

LOW_SCORE_COLOR = "#f38ba8"   # cells below 50


# ── Main Window ────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎓 Student Grade Calculator")
        self.setMinimumSize(900, 600)

        # locate students.txt next to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.students = load_students(os.path.join(base_dir, "students.txt"))

        self._build_ui()
        style_path = os.path.join(base_dir, "styles.qss")
        self.setStyleSheet(load_stylesheet(style_path))


    # ── UI Construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setSpacing(16)
        root.setContentsMargins(20, 20, 20, 20)

        # ── Input card ──
        input_card = QFrame()
        input_card.setObjectName("inputCard")
        card_layout = QVBoxLayout(input_card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(12)

        title = QLabel("ADD STUDENT")
        title.setObjectName("sectionTitle")
        card_layout.addWidget(title)

        # Row 1: Student ID + Name
        row1 = QHBoxLayout()
        row1.setSpacing(16)

        row1.addWidget(QLabel("Student ID:"))
        self.combo_id = QComboBox()
        self.combo_id.addItem("-- Select --")
        for sid in sorted(self.students.keys()):
            self.combo_id.addItem(sid)
        self.combo_id.currentTextChanged.connect(self._on_id_changed)
        row1.addWidget(self.combo_id)

        row1.addSpacing(24)
        row1.addWidget(QLabel("Student Name:"))
        self.lbl_name = QLabel("—")
        self.lbl_name.setObjectName("nameDisplay")
        self.lbl_name.setMinimumWidth(220)
        row1.addWidget(self.lbl_name)
        row1.addStretch()
        card_layout.addLayout(row1)

        # Row 2: Scores
        row2 = QHBoxLayout()
        row2.setSpacing(16)

        for label_text, attr in [("Math:", "spin_math"), ("Science:", "spin_sci"), ("English:", "spin_eng")]:
            row2.addWidget(QLabel(label_text))
            spin = QSpinBox()
            spin.setRange(0, 100)
            spin.setValue(0)
            setattr(self, attr, spin)
            row2.addWidget(spin)
            row2.addSpacing(8)

        row2.addStretch()
        card_layout.addLayout(row2)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.btn_add = QPushButton("＋  Add Student")
        self.btn_add.setObjectName("btnAdd")
        self.btn_add.clicked.connect(self._add_student)

        self.btn_reset = QPushButton("↺  Reset Input")
        self.btn_reset.setObjectName("btnReset")
        self.btn_reset.clicked.connect(self._reset_input)

        self.btn_clear = QPushButton("🗑  Clear All")
        self.btn_clear.setObjectName("btnClear")
        self.btn_clear.clicked.connect(self._clear_all)

        for btn in (self.btn_add, self.btn_reset, self.btn_clear):
            btn.setMinimumHeight(36)
            btn_row.addWidget(btn)

        btn_row.addStretch()
        card_layout.addLayout(btn_row)
        root.addWidget(input_card)

        # ── Table card ──
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(16, 16, 16, 16)
        table_layout.setSpacing(8)

        tbl_title = QLabel("STUDENT RECORDS")
        tbl_title.setObjectName("sectionTitle")
        table_layout.addWidget(tbl_title)

        headers = ["#", "Student ID", "Name", "Math", "Science", "English", "Total", "Average", "Grade"]
        self.table = QTableWidget(0, len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)

        # column widths
        for col, w in enumerate([40, 120, -1, 60, 70, 70, 60, 80, 60]):
            if w > 0:
                self.table.setColumnWidth(col, w)

        table_layout.addWidget(self.table)
        root.addWidget(table_card, stretch=1)

        # internal data store: {student_id: row_data}
        self._records: dict[str, dict] = {}

    # ── Slot Handlers ──────────────────────────────────────────────────────────

    def _on_id_changed(self, sid: str):
        name = self.students.get(sid, "")
        self.lbl_name.setText(name if name else "—")

    def _add_student(self):
        sid = self.combo_id.currentText()
        if sid == "-- Select --" or sid not in self.students:
            self.lbl_name.setText("⚠ Select a valid ID")
            return

        math_s = self.spin_math.value()
        sci_s = self.spin_sci.value()
        eng_s = self.spin_eng.value()
        total = math_s + sci_s + eng_s
        avg = total / 3
        grade = compute_grade(avg)

        self._records[sid] = {
            "name": self.students[sid],
            "math": math_s,
            "sci": sci_s,
            "eng": eng_s,
            "total": total,
            "avg": avg,
            "grade": grade,
        }
        self._refresh_table()

    def _reset_input(self):
        self.combo_id.setCurrentIndex(0)
        self.lbl_name.setText("—")
        self.spin_math.setValue(0)
        self.spin_sci.setValue(0)
        self.spin_eng.setValue(0)

    def _clear_all(self):
        self._records.clear()
        self.table.setRowCount(0)

    # ── Table Rendering ────────────────────────────────────────────────────────

    def _refresh_table(self):
        self.table.setRowCount(0)
        sorted_ids = sorted(self._records.keys())

        for row_idx, sid in enumerate(sorted_ids):
            r = self._records[sid]
            self.table.insertRow(row_idx)
            self.table.setRowHeight(row_idx, 36)

            values = [
                str(row_idx + 1),
                sid,
                r["name"],
                str(r["math"]),
                str(r["sci"]),
                str(r["eng"]),
                str(r["total"]),
                f"{r['avg']:.2f}",
                r["grade"],
            ]
            grade = r["grade"]
            is_fail = (grade == "F")

            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # row background for failing students
                if is_fail:
                    item.setBackground(QColor("#3d1a22"))
                    item.setForeground(QColor("#f38ba8"))

                # highlight low individual scores (< 50) in cols 3,4,5
                if col in (3, 4, 5) and int(val) < 50:
                    item.setBackground(QColor("#3d1a22"))
                    item.setForeground(QColor("#f38ba8"))

                # grade cell special color
                if col == 8:
                    colors = {
                        "A": ("#1a3d2b", "#a6e3a1"),
                        "B": ("#1a2a3d", "#89b4fa"),
                        "C": ("#2d1a3d", "#cba6f7"),
                        "D": ("#3d321a", "#f9e2af"),
                        "F": ("#3d1a22", "#f38ba8"),
                    }
                    bg, fg = colors.get(grade, ("#1e1e2e", "#cdd6f4"))
                    item.setBackground(QColor(bg))
                    item.setForeground(QColor(fg))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

                self.table.setItem(row_idx, col, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())