"""
Htun Htun Aung
683040750-7
Lab 5_5 P2
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor

from data import COURSES
from style import C, BASE, INPUT_SS, COMBO_SS, SCROLL_SS
from style import btn_ss, section_label, field_label, divider
from StudentCard import StudentCard


# ─────────────────────────────────────────────────────────────
#  Page 1 — Student List
# ─────────────────────────────────────────────────────────────
class StudentListPage(QWidget):

    go_to_add = Signal()

    def __init__(self):
        super().__init__()
        self._cards: list[StudentCard] = []
        self.setAcceptDrops(True)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── top bar ──
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)

        title = QLabel("Students")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet(f"color:{C['text']};")

        self.lbl_count = QLabel("0 enrolled")
        self.lbl_count.setStyleSheet(f"color:{C['muted']};font-size:13px;")

        btn_add = QPushButton("+ Add Student")
        btn_add.setCursor(QCursor(Qt.PointingHandCursor))
        btn_add.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        btn_add.clicked.connect(self.go_to_add.emit)

        bl.addWidget(title)
        bl.addSpacing(12)
        bl.addWidget(self.lbl_count, alignment=Qt.AlignVCenter)
        bl.addStretch()
        bl.addWidget(btn_add)

        # ── empty label ──
        self._lbl_empty = QLabel(
            "No students registered yet.\nClick \"+ Add Student\" to get started."
        )
        self._lbl_empty.setAlignment(Qt.AlignCenter)
        self._lbl_empty.setStyleSheet(f"color:{C['muted']};font-size:13px;")

        # ── scroll area ──
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet(SCROLL_SS)

        self._container = QWidget()
        self._container.setStyleSheet(f"background:{C['bg']};")
        self._card_lay = QVBoxLayout(self._container)
        self._card_lay.setContentsMargins(32, 16, 32, 16)
        self._card_lay.setSpacing(6)
        self._card_lay.addStretch()

        self._scroll.setWidget(self._container)
        self._scroll.setVisible(False)

        root.addWidget(bar)
        root.addWidget(self._lbl_empty, stretch=1)
        root.addWidget(self._scroll, stretch=1)

    # ── public ───────────────────────────────────────────────
    def add_student(self, data: dict):
        # create card and connect the delete signal
        card = StudentCard(data)
        card.delete_requested.connect(self._remove_card)

        # Add card to the list
        self._cards.append(card)

        # insert card before the trailing stretch
        self._card_lay.insertWidget(self._card_lay.count() - 1, card)

        self._refresh_count()
        self._refresh_empty()

    # ── private ──────────────────────────────────────────────
    def _remove_card(self, card: StudentCard):
        reply = QMessageBox.question(
            self, "Remove student",
            f"Remove {card.data['fullname']}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # remove card from the list
            self._cards.remove(card)
            # remove card from layout
            self._card_lay.removeWidget(card)
            card.deleteLater()
            self._refresh_count()
            self._refresh_empty()

    def _refresh_count(self):
        # get number of cards
        n = len(self._cards)
        # update number of student label
        self.lbl_count.setText(f"{n} enrolled")

    def _refresh_empty(self):
        has = bool(self._cards)
        self._lbl_empty.setVisible(not has)
        self._scroll.setVisible(has)

    # ── drag-drop reorder ────────────────────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "student_card":
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        src = event.source()
        if not isinstance(src, StudentCard) or src not in self._cards:
            return

        local_y = self._container.mapFrom(self, event.position().toPoint()).y()
        target = len(self._cards) - 1
        for i, card in enumerate(self._cards):
            if local_y < card.y() + card.height() // 2:
                target = i
                break

        src_idx = self._cards.index(src)
        if src_idx == target:
            return

        self._cards.pop(src_idx)
        self._cards.insert(target, src)
        for card in self._cards:
            self._card_lay.removeWidget(card)
        for i, card in enumerate(self._cards):
            self._card_lay.insertWidget(i, card)

        event.acceptProposedAction()


# ─────────────────────────────────────────────────────────────
#  Page 2 — Add Student Form
# ─────────────────────────────────────────────────────────────
class AddStudentPage(QWidget):

    # Signals for going back and going forward
    go_cancel = Signal()
    go_review = Signal(dict)

    def __init__(self):
        super().__init__()
        self._build()

    def _inp(self, ph: str = "") -> QLineEdit:
        e = QLineEdit()
        e.setPlaceholderText(ph)
        e.setMinimumHeight(38)
        e.setStyleSheet(INPUT_SS)
        return e

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Add Student")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        # scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(SCROLL_SS)

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── personal info ─────────────────────────────────────
        form.addWidget(section_label("Personal Information"))

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QLabel("Student ID *"), 0, 0)
        self.inp_id = self._inp("e.g. 65010001")
        grid.addWidget(self.inp_id, 0, 1, 1, 3)

        grid.addWidget(QLabel("First Name *"), 1, 0)
        self.inp_fn = self._inp("First name")
        grid.addWidget(self.inp_fn, 1, 1)
        grid.addWidget(QLabel("Last Name *"), 1, 2)
        self.inp_ln = self._inp("Last name")
        grid.addWidget(self.inp_ln, 1, 3)

        grid.addWidget(QLabel("Faculty *"), 2, 0)
        self.inp_fac = self._inp("e.g. Science & Technology")
        grid.addWidget(self.inp_fac, 2, 1)
        grid.addWidget(QLabel("Major *"), 2, 2)
        self.inp_maj = self._inp("e.g. Computer Science")
        grid.addWidget(self.inp_maj, 2, 3)

        form.addLayout(grid)
        form.addWidget(divider())

        # ── course selection ──────────────────────────────────
        form.addWidget(section_label("Course Selection  (choose 1–3)"))

        self._course_combos: list[QComboBox] = []
        for i in range(1, 4):
            row = QHBoxLayout()
            lbl = QLabel(f"Course {i}")
            lbl.setFixedWidth(80)
            combo = QComboBox()
            combo.addItems(COURSES)
            combo.setMinimumHeight(38)
            combo.setStyleSheet(COMBO_SS)
            row.addWidget(lbl)
            row.addWidget(combo)
            form.addLayout(row)
            self._course_combos.append(combo)

        # ── error label ───────────────────────────────────────
        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet(f"color:{C['red']};font-size:13px;")
        form.addWidget(self.lbl_err)

        form.addStretch()

        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        bc = QPushButton("← Cancel")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )
        bc.clicked.connect(self._on_cancel)

        br = QPushButton("Review →")
        br.setCursor(QCursor(Qt.PointingHandCursor))
        br.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        br.clicked.connect(self._on_review)

        btn_row.addWidget(bc)
        btn_row.addStretch()
        btn_row.addWidget(br)
        form.addLayout(btn_row)

        scroll.setWidget(body)
        root.addWidget(bar)
        root.addWidget(scroll, stretch=1)

    def _on_cancel(self):
        self.clear_form()
        self.go_cancel.emit()

    def _on_review(self):
        # check for field errors / incomplete
        errors = []
        if not self.inp_id.text().strip():  errors.append("Student ID")
        if not self.inp_fn.text().strip():  errors.append("First Name")
        if not self.inp_ln.text().strip():  errors.append("Last Name")
        if not self.inp_fac.text().strip(): errors.append("Faculty")
        if not self.inp_maj.text().strip(): errors.append("Major")

        selected = [c.currentText() for c in self._course_combos
                    if c.currentText() != "— Select Course —"]
        if not selected:
            errors.append("at least 1 course")

        # Warn the user if needed
        if errors:
            self.lbl_err.setText("Required: " + ",  ".join(errors))
            return

        self.lbl_err.setText("")

        # emit signal with data
        data = {
            "student_id": self.inp_id.text().strip(),
            "first_name": self.inp_fn.text().strip(),
            "last_name":  self.inp_ln.text().strip(),
            "faculty":    self.inp_fac.text().strip(),
            "major":      self.inp_maj.text().strip(),
            "course1":    self._course_combos[0].currentText(),
            "course2":    self._course_combos[1].currentText(),
            "course3":    self._course_combos[2].currentText(),
        }
        self.go_review.emit(data)

    def load_data(self, d: dict):
        """Pre-fill form when user clicks Edit on Page 3."""
        self.inp_id.setText(d.get("student_id", ""))
        self.inp_fn.setText(d.get("first_name", ""))
        self.inp_ln.setText(d.get("last_name", ""))
        self.inp_fac.setText(d.get("faculty", ""))
        self.inp_maj.setText(d.get("major", ""))
        for i, combo in enumerate(self._course_combos):
            val = d.get(f"course{i+1}", "— Select Course —")
            idx = combo.findText(val)
            combo.setCurrentIndex(idx if idx >= 0 else 0)

    def clear_form(self):
        for w in (self.inp_id, self.inp_fn, self.inp_ln, self.inp_fac, self.inp_maj):
            w.clear()
        for combo in self._course_combos:
            combo.setCurrentIndex(0)
        self.lbl_err.setText("")


# ─────────────────────────────────────────────────────────────
#  Page 3 — Review & Confirm
# ─────────────────────────────────────────────────────────────
class ReviewPage(QWidget):

    # Signals for confirming and going back to edit
    go_edit    = Signal()
    go_confirm = Signal(dict)

    def __init__(self):
        super().__init__()
        self._data: dict = {}
        self._build()

    def _row(self, layout: QVBoxLayout, label: str) -> QLabel:
        row = QHBoxLayout()
        row.setSpacing(0)
        lbl = QLabel(label)
        lbl.setFixedWidth(130)
        lbl.setStyleSheet(f"color:{C['muted']};font-size:13px;")
        val = QLabel("—")
        val.setStyleSheet(f"color:{C['text']};font-size:13px;")
        val.setWordWrap(True)
        row.addWidget(lbl)
        row.addWidget(val, stretch=1)
        layout.addLayout(row)
        return val

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Review & Confirm")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── summary section ───────────────────────────────────
        form.addWidget(section_label("Student Information"))

        self.val_id      = self._row(form, "Student ID")
        self.val_name    = self._row(form, "Full Name")
        self.val_faculty = self._row(form, "Faculty")
        self.val_major   = self._row(form, "Major")

        form.addWidget(divider())
        form.addWidget(section_label("Courses"))

        self.val_c1 = self._row(form, "Course 1")
        self.val_c2 = self._row(form, "Course 2")
        self.val_c3 = self._row(form, "Course 3")

        form.addStretch()

        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        be = QPushButton("← Edit")
        be.setCursor(QCursor(Qt.PointingHandCursor))
        be.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )
        be.clicked.connect(self.go_edit.emit)

        bc = QPushButton("Confirm Registration")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(btn_ss(C['green'], "#15803d"))
        bc.clicked.connect(lambda: self.go_confirm.emit(self._data))

        btn_row.addWidget(be)
        btn_row.addStretch()
        btn_row.addWidget(bc)
        form.addLayout(btn_row)

        root.addWidget(bar)
        root.addWidget(body, stretch=1)

    def load_data(self, d: dict):
        """Fill review page with data from Page 2."""
        self._data = d
        self.val_id.setText(d.get("student_id", "—"))
        fullname = f"{d.get('first_name', '')} {d.get('last_name', '')}".strip()
        self.val_name.setText(fullname or "—")
        self.val_name.setStyleSheet(f"color:{C['accent']};font-size:13px;font-weight:600;")
        self.val_faculty.setText(d.get("faculty", "—"))
        self.val_major.setText(d.get("major", "—"))

        for val_lbl, key in [
            (self.val_c1, "course1"),
            (self.val_c2, "course2"),
            (self.val_c3, "course3"),
        ]:
            v = d.get(key, "")
            if v and v != "— Select Course —":
                val_lbl.setText(v)
                val_lbl.setStyleSheet(f"color:{C['accent']};font-size:13px;")
            else:
                val_lbl.setText("—")
                val_lbl.setStyleSheet(f"color:{C['text']};font-size:13px;")


# ─────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.setMinimumSize(860, 580)
        self.resize(980, 660)
        self.setStyleSheet(BASE)
        self._build()

    def _build(self):
        central = QWidget()
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self.setCentralWidget(central)

        # Pages
        self.p1 = StudentListPage()
        self.p2 = AddStudentPage()
        self.p3 = ReviewPage()

        # Stack
        self.stack = QStackedWidget()
        self.stack.addWidget(self.p1)   # index 0
        self.stack.addWidget(self.p2)   # index 1
        self.stack.addWidget(self.p3)   # index 2

        outer.addWidget(self.stack)

        # Signals
        self.p1.go_to_add.connect(lambda: self.stack.setCurrentIndex(1))
        self.p2.go_cancel.connect(lambda: self.stack.setCurrentIndex(0))
        self.p2.go_review.connect(self._on_go_review)
        self.p3.go_edit.connect(self._on_go_edit)
        self.p3.go_confirm.connect(self._on_confirm)

    # ── helpers ──────────────────────────────────────────────
    def _on_go_review(self, data: dict):
        self.p3.load_data(data)
        self.stack.setCurrentIndex(2)

    def _on_go_edit(self):
        self.p2.load_data(self.p3._data)
        self.stack.setCurrentIndex(1)

    def _on_confirm(self, data: dict):
        self.p1.add_student(data)
        self.p2.clear_form()
        self.stack.setCurrentIndex(0)

        # Success dialog
        msg = QMessageBox(self)
        msg.setWindowTitle("Registration Successful")
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            f"<b style='color:{C['green']};font-size:15px;'>Registration Successful!</b><br><br>"
            f"<b>{data['first_name']} {data['last_name']}</b> has been registered."
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())