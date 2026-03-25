"""
Htun Htun Aung
683040750-7
P1 Lab5_4
"""

import sys
import os
import pyperclip
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QSpinBox, QComboBox, QPushButton, QTextEdit, QStatusBar,
    QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout, QFrame,
    QToolBar, QFileDialog, QColorDialog, QSizePolicy, QStyle
)
from PySide6.QtGui import QFont, QColor, QIcon, QPalette, QAction, QPixmap
from PySide6.QtCore import Qt, QSize

POSITIONS = ["Choose your position", "Student", "Developer", "Designer",
             "Manager", "Teacher", "Engineer", "Other"]

dir_path = os.path.dirname(os.path.abspath(__file__))
default_color = "#B0E0E6"

QSS = open(os.path.join(dir_path, "P1_style.qss")).read() if os.path.exists(
    os.path.join(dir_path, "P1_style.qss")) else ""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Personal Info Card")
        self.setMinimumWidth(480)
        self.setGeometry(100, 100, 480, 520)
        self.fav_color = QColor(default_color)
        self.card_generated = False   # tracks whether Generate has been clicked
        self.last_save = None         # tracks last saved file path
        self._build_menu()
        self._build_toolbar()
        self._build_ui()
        self._build_statusbar()

    # ── Menu ──────────────────────────────────────────────
    def _build_menu(self):
        mb = self.menuBar()

        file_menu = mb.addMenu("File")
        for text, slot, shortcut in [
            ("Generate Card", self.generate_card, "Ctrl+G"),
            ("Save Card",     self.save_card,     "Ctrl+S"),
            ("Clear Display", self.clear_display, "Ctrl+D"),
            ("Exit",          self.close,         "Ctrl+Q"),
        ]:
            act = QAction(text, self)
            act.triggered.connect(slot)
            act.setShortcut(shortcut)
            file_menu.addAction(act)

        edit_menu = mb.addMenu("Edit")
        for text, slot, shortcut in [
            ("Copy Card",  self.copy_card,  "Ctrl+Shift+C"),
            ("Clear Form", self.clear_form, "Ctrl+R"),
        ]:
            act = QAction(text, self)
            act.triggered.connect(slot)
            act.setShortcut(shortcut)
            edit_menu.addAction(act)

    # ── Toolbar ───────────────────────────────────────────
    def _build_toolbar(self):
        tb = QToolBar("Main Toolbar")
        tb.setIconSize(QSize(28, 28))
        tb.setMovable(False)
        self.addToolBar(tb)

        base = dir_path

        def make_action(icon_file, std_icon, fallback_text, tooltip, slot):
            icon_path = os.path.join(base, icon_file)
            if os.path.exists(icon_path):
                act = QAction(QIcon(icon_path), "", self)
            else:
                act = QAction(self.style().standardIcon(std_icon), fallback_text, self)
            act.setToolTip(tooltip)
            act.triggered.connect(slot)
            return act

        tb.addAction(make_action("generate.jpg",  QStyle.SP_DialogApplyButton,   "▶", "Generate Card",        self.generate_card))
        tb.addAction(make_action("save_card.png", QStyle.SP_DialogSaveButton,    "💾", "Save Card",            self.save_card))
        tb.addAction(make_action("Delete.png",    QStyle.SP_DialogDiscardButton, "🗑", "Clear Form & Display", self.clear_all))

    # ── Central UI ────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # ---- INPUT SECTION ----
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(8)
        form_layout.setHorizontalSpacing(12)

        self.le_name = QLineEdit()
        self.le_name.setPlaceholderText("First name and Lastname")
        form_layout.addRow("Full name:", self.le_name)

        self.sp_age = QSpinBox()
        self.sp_age.setRange(1, 120)
        self.sp_age.setValue(25)
        form_layout.addRow("Age:", self.sp_age)

        self.le_email = QLineEdit()
        self.le_email.setPlaceholderText("username@domain.name")
        form_layout.addRow("Email:", self.le_email)

        self.cb_position = QComboBox()
        self.cb_position.addItems(POSITIONS)
        self.cb_position.setCurrentIndex(0)
        form_layout.addRow("Position:", self.cb_position)

        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(28, 28)
        self._update_swatch()
        self.btn_color = QPushButton("Pick Color")
        self.btn_color.clicked.connect(self.pick_color)
        color_row = QHBoxLayout()
        color_row.addWidget(self.color_swatch)
        color_row.addWidget(self.btn_color)
        color_row.addStretch()
        color_widget = QWidget()
        color_widget.setLayout(color_row)
        form_layout.addRow("Favorite color:", color_widget)

        root.addLayout(form_layout)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet("background-color: #cccccc;")
        root.addWidget(sep)

        # ---- CARD DISPLAY SECTION ----
        self.card_display = QWidget()
        self.card_display.setMinimumHeight(140)
        card_layout = QVBoxLayout(self.card_display)
        card_layout.setContentsMargins(16, 12, 16, 12)
        card_layout.setSpacing(4)

        self.lbl_card_name = QLabel("Your name here")
        f = QFont()
        f.setPointSize(16)
        f.setBold(True)
        self.lbl_card_name.setFont(f)

        self.lbl_card_age = QLabel("(Age)")

        self.lbl_card_position = QLabel("Your position here")
        fp = QFont()
        fp.setPointSize(12)
        self.lbl_card_position.setFont(fp)

        # Email row with icon
        self.lbl_card_email = QLabel("your_username@domain.name")
        email_icon = QLabel()
        mail_icon_path = os.path.join(dir_path, "mail.png")
        if os.path.exists(mail_icon_path):
            email_icon.setPixmap(QPixmap(mail_icon_path).scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            email_icon.setText("✉")
        email_row = QHBoxLayout()
        email_row.addWidget(email_icon)
        email_row.addWidget(self.lbl_card_email)
        email_row.addStretch()

        card_layout.addWidget(self.lbl_card_name)
        card_layout.addWidget(self.lbl_card_age)
        card_layout.addStretch()
        card_layout.addWidget(self.lbl_card_position)
        card_layout.addLayout(email_row)
        card_layout.addSpacing(10)

        self._apply_card_bg(self.fav_color)
        root.addWidget(self.card_display)

    # ── Status bar ────────────────────────────────────────
    def _build_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Fill in your details and click generate")

    # ── Helpers ───────────────────────────────────────────
    def _update_swatch(self):
        self.color_swatch.setStyleSheet(
            f"background:{self.fav_color.name()}; border:1px solid #aaa; border-radius:4px;")

    def _apply_card_bg(self, color: QColor):
        self.card_display.setStyleSheet(
            f"QWidget {{ background-color:{color.name()}; border-radius:8px; }}")
        r, g, b = color.red(), color.green(), color.blue()
        dark = f"rgb({r//2},{g//2},{b//2})"
        for lbl in (self.lbl_card_name, self.lbl_card_age,
                    self.lbl_card_position, self.lbl_card_email):
            lbl.setStyleSheet(f"color:{dark}; background:transparent;")

    def _card_text(self):
        return (
            f"{self.lbl_card_name.text()}\n"
            f"{self.lbl_card_age.text()}\n"
            f"{self.lbl_card_position.text()}\n"
            f"{self.lbl_card_email.text()}\n"
        )

    # ── Actions ───────────────────────────────────────────
    def pick_color(self):
        color = QColorDialog.getColor(self.fav_color, self, "Pick Favorite Color")
        if color.isValid():
            self.fav_color = color
            self._update_swatch()
            if self.card_generated:
                self._apply_card_bg(color)
                self.status.showMessage("Color updated", 3000)
            else:
                self.status.showMessage("Color selected – generate the card to apply it", 3000)

    def generate_card(self):
        # Validation: name, email format, position
        if not self.le_name.text().strip() or not self.le_email.text().strip():
            self.status.showMessage("Please fill in all fields with valid data", 3000)
            return
        if "@" not in self.le_email.text():
            self.status.showMessage("Please enter a valid email address", 3000)
            return
        if self.cb_position.currentIndex() == 0:
            self.status.showMessage("Please select a position", 3000)
            return

        name  = self.le_name.text().strip()
        age   = self.sp_age.value()
        pos   = self.cb_position.currentText()
        email = self.le_email.text().strip()

        self.lbl_card_name.setText(name)
        self.lbl_card_age.setText(f"({age})")
        self.lbl_card_position.setText(pos)
        self.lbl_card_email.setText(email)
        self._apply_card_bg(self.fav_color)
        self.card_generated = True
        self.status.showMessage("Card generated", 3000)

    def save_card(self):
        if not self.card_generated:
            self.status.showMessage("Generate a card first before saving!", 3000)
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Save Card", "my_card.txt", "Text Files (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self._card_text())
            self.last_save = filename
            self.status.showMessage(f"Saved: {os.path.basename(filename)}", 3000)

    def copy_card(self):
        if not self.card_generated:
            self.status.showMessage("Generate a card first before copying!", 3000)
            return
        try:
            pyperclip.copy(self._card_text())
            self.status.showMessage("Card copied to clipboard", 3000)
        except Exception:
            self.status.showMessage("Copy failed – pyperclip not available", 3000)

    def clear_display(self):
        self.card_generated = False   # reset FIRST
        self.lbl_card_name.setText("Your name here")
        self.lbl_card_age.setText("(Age)")
        self.lbl_card_position.setText("Your position here")
        self.lbl_card_email.setText("your_username@domain.name")
        self._apply_card_bg(QColor(default_color))
        self.status.showMessage("Display cleared", 3000)

    def clear_form(self):
        self.card_generated = False   # reset FIRST

        # Block signals so clearing fields doesn't wipe the card display
        for widget in (self.le_name, self.le_email, self.sp_age, self.cb_position):
            widget.blockSignals(True)

        self.le_name.clear()
        self.sp_age.setValue(25)
        self.le_email.clear()
        self.cb_position.setCurrentIndex(0)

        for widget in (self.le_name, self.le_email, self.sp_age, self.cb_position):
            widget.blockSignals(False)

        self.fav_color = QColor(default_color)
        self._update_swatch()
        self.status.showMessage("Form cleared", 3000)

    def clear_all(self):
        self.clear_form()
        self.clear_display()
        self.status.showMessage("Form and display cleared", 3000)


def main():
    sys.argv += ['-platform', 'windows:darkmode=1']
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    if QSS:
        app.setStyleSheet(QSS)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()