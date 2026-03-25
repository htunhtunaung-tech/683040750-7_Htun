"""
Htun Htun Aung
683040750-7
P1 Lab5_4
"""

import sys
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QSlider, QSpinBox, QPushButton,
    QFrame, QProgressBar, QFileDialog, QStatusBar, QMenuBar,
    QToolBar, QMessageBox, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import (
    QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QAction
)


# ── colour tokens ──────────────────────────────────────────────────────────────
BG_LEFT   = "#f5f4f8"
BG_RIGHT  = "#1a1b2e"
ACCENT    = "#7c5cbf"
ACCENT2   = "#a97de8"
TEXT_DARK = "#1a1b2e"
TEXT_LITE = "#e8e0f7"
MUTED     = "#9990b0"
RED_WARN  = "#e05252"
GREEN_OK  = "#52b788"

RACES   = ["Human", "Elf", "Dwarf", "Orc", "Undead"]
CLASSES = ["Warrior", "Mage", "Rogue", "Paladin", "Ranger"]
GENDERS = ["Male", "Female", "Other"]

STAT_ICONS = {"STR": "⚔", "DEX": "🏹", "INT": "🔮", "VIT": "❤"}

STAT_COLORS = {
    "STR": "#e05252",
    "DEX": "#52b788",
    "INT": "#5b8dd9",
    "VIT": "#e8a23a",
}

MAX_POINTS = 40
DEFAULT_STAT = 5


# ── tiny icon factory (coloured Unicode-based QPixmap) ─────────────────────────
def _make_icon(text: str, fg: str = "#ffffff", bg: str = ACCENT,
               size: int = 28) -> QIcon:
    pix = QPixmap(size, size)
    pix.fill(QColor(bg))
    p = QPainter(pix)
    p.setRenderHint(QPainter.TextAntialiasing)
    p.setPen(QColor(fg))
    font = QFont("Segoe UI Emoji", int(size * 0.44))
    p.setFont(font)
    p.drawText(pix.rect(), Qt.AlignCenter, text)
    p.end()
    return QIcon(pix)


# ── stat row (label + slider + spinbox) ────────────────────────────────────────
class StatRow(QWidget):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.name = name
        self._building = False

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 2, 0, 2)
        lay.setSpacing(8)

        icon_lbl = QLabel(STAT_ICONS[name])
        icon_lbl.setFixedWidth(22)
        icon_lbl.setFont(QFont("Segoe UI Emoji", 13))
        lay.addWidget(icon_lbl)

        name_lbl = QLabel(name)
        name_lbl.setFixedWidth(30)
        name_lbl.setFont(QFont("Segoe UI Semibold", 10, QFont.Bold))
        name_lbl.setStyleSheet(f"color:{STAT_COLORS[name]};")
        lay.addWidget(name_lbl)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 20)
        self.slider.setValue(DEFAULT_STAT)
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 6px; border-radius: 3px;
                background: #d5cce8;
            }}
            QSlider::sub-page:horizontal {{
                background: {STAT_COLORS[name]};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                width: 14px; height: 14px; margin: -4px 0;
                border-radius: 7px;
                background: {STAT_COLORS[name]};
                border: 2px solid white;
            }}
        """)
        lay.addWidget(self.slider, stretch=1)

        self.spin = QSpinBox()
        self.spin.setRange(1, 20)
        self.spin.setValue(DEFAULT_STAT)
        self.spin.setFixedWidth(46)
        self.spin.setAlignment(Qt.AlignCenter)
        self.spin.setStyleSheet(f"""
            QSpinBox {{
                border: 1.5px solid {STAT_COLORS[name]};
                border-radius: 5px;
                padding: 2px 0;
                font-weight: bold;
                color: {STAT_COLORS[name]};
                background: #f5f4f8;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{ width: 14px; }}
        """)
        lay.addWidget(self.spin)

        self.slider.valueChanged.connect(self._slider_changed)
        self.spin.valueChanged.connect(self._spin_changed)

    def _slider_changed(self, v):
        if not self._building:
            self._building = True
            self.spin.setValue(v)
            self._building = False

    def _spin_changed(self, v):
        if not self._building:
            self._building = True
            self.slider.setValue(v)
            self._building = False

    def value(self) -> int:
        return self.spin.value()

    def set_value(self, v: int):
        self.spin.setValue(v)

    def connect_changed(self, slot):
        self.spin.valueChanged.connect(slot)


# ── right-panel stat bar row ────────────────────────────────────────────────────
class SheetStatBar(QWidget):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 2, 8, 2)
        lay.setSpacing(6)

        lbl = QLabel(name)
        lbl.setFixedWidth(30)
        lbl.setFont(QFont("Segoe UI Semibold", 9, QFont.Bold))
        lbl.setStyleSheet(f"color:{STAT_COLORS[name]};")
        lay.addWidget(lbl)

        self.bar = QProgressBar()
        self.bar.setRange(0, 20)
        self.bar.setValue(0)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(10)
        self.bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background: #2d2f4a;
            }}
            QProgressBar::chunk {{
                border-radius: 4px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {STAT_COLORS[name]}, stop:1 {ACCENT2});
            }}
        """)
        lay.addWidget(self.bar, stretch=1)

        self.val_lbl = QLabel("—")
        self.val_lbl.setFixedWidth(22)
        self.val_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.val_lbl.setFont(QFont("Consolas", 9, QFont.Bold))
        self.val_lbl.setStyleSheet(f"color:{STAT_COLORS[name]};")
        lay.addWidget(self.val_lbl)

    def update_value(self, v: int):
        self.bar.setValue(v)
        self.val_lbl.setText(str(v))


# ── main window ────────────────────────────────────────────────────────────────
class CharacterBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Character Builder")
        self.setMinimumSize(720, 500)
        self._build_ui()
        self._build_menu()
        self._build_toolbar()
        self._build_statusbar()
        self._update_points()
        self.show_status("Ready — create your character", color=MUTED)

    # ── UI ──────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── LEFT panel ──────────────────────────────────────────────────────────
        left = QWidget()
        left.setStyleSheet(f"background:{BG_LEFT};")
        llay = QVBoxLayout(left)
        llay.setContentsMargins(20, 16, 20, 16)
        llay.setSpacing(10)

        # ── form fields ─────────────────────────────────────────────────────────
        def field_row(label_text, widget):
            row = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setFixedWidth(110)
            lbl.setFont(QFont("Segoe UI", 10))
            lbl.setStyleSheet(f"color:{TEXT_DARK};")
            row.addWidget(lbl)
            row.addWidget(widget, stretch=1)
            return row

        field_style = f"""
            border: 1.5px solid #d5cce8;
            border-radius: 6px;
            padding: 5px 10px;
            background: white;
            font-family: 'Segoe UI';
            font-size: 10pt;
            color: {TEXT_DARK};
        """
        combo_style = field_style + """
            QComboBox::drop-down { border: none; width: 22px; }
            QComboBox QAbstractItemView { border: 1px solid #d5cce8; }
        """

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter character name...")
        self.name_edit.setStyleSheet(field_style)
        llay.addLayout(field_row("Character Name:", self.name_edit))

        self.race_combo = QComboBox()
        self.race_combo.addItem("Choose race")
        self.race_combo.addItems(RACES)
        self.race_combo.setStyleSheet(combo_style)
        llay.addLayout(field_row("Race:", self.race_combo))

        self.class_combo = QComboBox()
        self.class_combo.addItem("Choose class")
        self.class_combo.addItems(CLASSES)
        self.class_combo.setStyleSheet(combo_style)
        llay.addLayout(field_row("Class:", self.class_combo))

        self.gender_combo = QComboBox()
        self.gender_combo.addItem("Choose gender")
        self.gender_combo.addItems(GENDERS)
        self.gender_combo.setStyleSheet(combo_style)
        llay.addLayout(field_row("Gender:", self.gender_combo))

        # divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color:#d5cce8;")
        llay.addWidget(div)

        # ── stat allocation ──────────────────────────────────────────────────────
        stat_header = QLabel("Stat Allocation")
        stat_header.setFont(QFont("Segoe UI Semibold", 11, QFont.Bold))
        stat_header.setStyleSheet(f"color:{ACCENT};")
        llay.addWidget(stat_header)

        self.stat_rows: dict[str, StatRow] = {}
        for stat in ("STR", "DEX", "INT", "VIT"):
            row = StatRow(stat)
            row.connect_changed(self._update_points)
            self.stat_rows[stat] = row
            llay.addWidget(row)

        self.points_lbl = QLabel("Points used: 20 / 40")
        self.points_lbl.setFont(QFont("Segoe UI Semibold", 10, QFont.Bold))
        self.points_lbl.setStyleSheet(f"color:{TEXT_DARK};")
        llay.addWidget(self.points_lbl)

        # generate button
        self.gen_btn = QPushButton("  ⚔  Generate Character Sheet")
        self.gen_btn.setFont(QFont("Segoe UI Semibold", 11, QFont.Bold))
        self.gen_btn.setCursor(Qt.PointingHandCursor)
        self.gen_btn.setFixedHeight(42)
        self.gen_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
            }}
            QPushButton:hover {{
                background: {ACCENT2};
            }}
            QPushButton:pressed {{
                background: #5a3fa0;
            }}
        """)
        self.gen_btn.clicked.connect(self.generate_sheet)
        llay.addWidget(self.gen_btn)
        llay.addStretch()

        root.addWidget(left, stretch=1)

        # ── RIGHT panel ─────────────────────────────────────────────────────────
        right = QWidget()
        right.setFixedWidth(250)
        right.setStyleSheet(f"background:{BG_RIGHT}; border-left: 2px solid #2d2f4a;")
        rlay = QVBoxLayout(right)
        rlay.setContentsMargins(14, 20, 14, 20)
        rlay.setSpacing(8)

        # decorative top rule
        top_rule = QLabel("— Character Name —")
        top_rule.setAlignment(Qt.AlignCenter)
        self.sheet_name = top_rule
        top_rule.setFont(QFont("Cinzel Decorative", 12, QFont.Bold) if
                         QFont("Cinzel Decorative").exactMatch() else
                         QFont("Georgia", 12, QFont.Bold))
        top_rule.setStyleSheet(f"color:{ACCENT2}; letter-spacing: 1px;")
        top_rule.setWordWrap(True)
        rlay.addWidget(top_rule)

        self.sheet_subline = QLabel("Race  •  Class")
        self.sheet_subline.setAlignment(Qt.AlignCenter)
        self.sheet_subline.setFont(QFont("Segoe UI", 9))
        self.sheet_subline.setStyleSheet(f"color:{MUTED};")
        rlay.addWidget(self.sheet_subline)

        # gender badge
        self.sheet_gender = QLabel("")
        self.sheet_gender.setAlignment(Qt.AlignCenter)
        self.sheet_gender.setFont(QFont("Segoe UI", 8))
        self.sheet_gender.setStyleSheet(f"color:{MUTED};")
        rlay.addWidget(self.sheet_gender)

        div2 = QFrame()
        div2.setFrameShape(QFrame.HLine)
        div2.setStyleSheet(f"color:#2d2f4a;")
        rlay.addWidget(div2)

        self.sheet_bars: dict[str, SheetStatBar] = {}
        for stat in ("STR", "DEX", "INT", "VIT"):
            bar = SheetStatBar(stat)
            self.sheet_bars[stat] = bar
            rlay.addWidget(bar)

        rlay.addStretch()

        # flavour quote
        self.flavor_lbl = QLabel("")
        self.flavor_lbl.setAlignment(Qt.AlignCenter)
        self.flavor_lbl.setWordWrap(True)
        self.flavor_lbl.setFont(QFont("Georgia", 8, italic=True))
        self.flavor_lbl.setStyleSheet(f"color:{MUTED}; font-style:italic;")
        rlay.addWidget(self.flavor_lbl)

        root.addWidget(right)

    # ── MENU BAR ────────────────────────────────────────────────────────────────
    def _build_menu(self):
        mb = self.menuBar()
        mb.setStyleSheet(f"""
            QMenuBar {{ background:{BG_LEFT}; color:{TEXT_DARK}; font-family:'Segoe UI'; font-size:10pt; }}
            QMenuBar::item:selected {{ background:{ACCENT}; color:white; border-radius:4px; }}
            QMenu {{ background:white; color:{TEXT_DARK}; border:1px solid #d5cce8; font-family:'Segoe UI'; font-size:10pt; }}
            QMenu::item:selected {{ background:{ACCENT}; color:white; }}
        """)

        game = mb.addMenu("Game")
        game.addAction("New Character", self.new_character, "Ctrl+N")
        game.addAction("Generate Sheet", self.generate_sheet, "Ctrl+G")
        game.addAction("Save Sheet", self.save_sheet, "Ctrl+S")
        game.addSeparator()
        game.addAction("Exit", self.close, "Ctrl+Q")

        edit = mb.addMenu("Edit")
        edit.addAction("Reset Stats", self.reset_stats)
        edit.addAction("Randomize", self.randomize)

    # ── TOOLBAR ─────────────────────────────────────────────────────────────────
    def _build_toolbar(self):
        tb = QToolBar("Main Toolbar")
        tb.setMovable(False)
        tb.setIconSize(QSize(22, 22))
        tb.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        tb.setStyleSheet(f"""
            QToolBar {{ background:{BG_LEFT}; border-bottom:1px solid #d5cce8; spacing:2px; padding:3px 6px; }}
            QToolButton {{
                border-radius:6px; padding:4px 10px 4px 6px;
                color:{TEXT_DARK}; font-size:9pt; font-family:'Segoe UI';
                spacing:5px;
            }}
            QToolButton:hover {{ background:#e8e0f7; }}
            QToolButton:pressed {{ background:#d5cce8; }}
        """)
        self.addToolBar(tb)

        acts = [
            (_make_icon("✦", bg=ACCENT),    "New",        self.new_character),
            (_make_icon("⚔", bg="#5b8dd9"), "Generate",   self.generate_sheet),
            (_make_icon("🎲", bg=GREEN_OK), "Randomize",  self.randomize),
            (_make_icon("💾", bg="#e8a23a"), "Save",       self.save_sheet),
        ]
        for icon, label, slot in acts:
            act = QAction(icon, label, self)
            act.setToolTip(label)
            act.triggered.connect(slot)
            tb.addAction(act)

    # ── STATUS BAR ──────────────────────────────────────────────────────────────
    def _build_statusbar(self):
        sb = self.statusBar()
        sb.setStyleSheet(f"""
            QStatusBar {{ background:{BG_LEFT}; color:{MUTED}; font-size:9pt; border-top:1px solid #d5cce8; }}
            QStatusBar::item {{ border: none; }}
        """)
        self._temp_lbl = QLabel("")
        sb.addWidget(self._temp_lbl, stretch=1)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(lambda: self._temp_lbl.setText(""))

    def show_status(self, msg: str, color: str = TEXT_DARK, duration: int = 4000):
        self._temp_lbl.setText(msg)
        self._temp_lbl.setStyleSheet(f"color:{color}; padding-left:4px;")
        if duration:
            self._timer.start(duration)

    # ── LOGIC ───────────────────────────────────────────────────────────────────
    def _update_points(self):
        total = sum(r.value() for r in self.stat_rows.values())
        color = RED_WARN if total > MAX_POINTS else TEXT_DARK
        self.points_lbl.setText(f"Points used: {total} / {MAX_POINTS}")
        self.points_lbl.setStyleSheet(f"color:{color}; font-weight:bold;")

    def _total_points(self) -> int:
        return sum(r.value() for r in self.stat_rows.values())

    def new_character(self):
        self.name_edit.clear()
        self.race_combo.setCurrentIndex(0)
        self.class_combo.setCurrentIndex(0)
        self.gender_combo.setCurrentIndex(0)
        self.reset_stats()
        # clear sheet panel
        self.sheet_name.setText("— Character Name —")
        self.sheet_subline.setText("Race  •  Class")
        self.sheet_gender.setText("")
        self.flavor_lbl.setText("")
        for bar in self.sheet_bars.values():
            bar.update_value(0)
        self.show_status("✦  New character started.", color=ACCENT)

    def reset_stats(self):
        for row in self.stat_rows.values():
            row.set_value(DEFAULT_STAT)
        self._update_points()
        self.show_status("↺  Stats reset to default (5).", color=MUTED)

    def randomize(self):
        # random name
        prefixes = ["Aer", "Bel", "Cal", "Dor", "Eld", "Fyr", "Gar", "Hel",
                    "Ith", "Jor", "Kel", "Lyr", "Mor", "Nyx", "Orm", "Pyr"]
        suffixes = ["ath", "ion", "dra", "fel", "wyn", "mir", "os", "iel",
                    "ven", "thas", "ris", "dan", "tor", "val", "nar", "ax"]
        self.name_edit.setText(random.choice(prefixes) + random.choice(suffixes))

        self.race_combo.setCurrentIndex(random.randint(1, len(RACES)))
        self.class_combo.setCurrentIndex(random.randint(1, len(CLASSES)))
        self.gender_combo.setCurrentIndex(random.randint(1, len(GENDERS)))

        # distribute up to 40 points across 4 stats (each 1–20)
        vals = [1, 1, 1, 1]
        remaining = MAX_POINTS - 4
        for i in range(3):
            mx = min(19, remaining - (3 - i))
            add = random.randint(0, mx)
            vals[i] += add
            remaining -= add
        vals[3] += remaining

        random.shuffle(vals)
        for row, v in zip(self.stat_rows.values(), vals):
            row.set_value(v)

        self._update_points()
        self.show_status("🎲  Character randomized!", color=GREEN_OK)

    def generate_sheet(self):
        name = self.name_edit.text().strip() or "Unknown Hero"
        race = self.race_combo.currentText()
        cls  = self.class_combo.currentText()
        gender = self.gender_combo.currentText()

        if race == "Choose race":   race = "Unknown Race"
        if cls  == "Choose class":  cls  = "Unknown Class"
        if gender == "Choose gender": gender = ""

        if self._total_points() > MAX_POINTS:
            self.show_status("⚠  Stat total exceeds 40! Reduce stats first.", color=RED_WARN)
            return

        self.sheet_name.setText(f"— {name} —")
        self.sheet_subline.setText(f"{race}  •  {cls}")
        self.sheet_gender.setText(gender)

        for stat, row in self.stat_rows.items():
            self.sheet_bars[stat].update_value(row.value())

        flavors = {
            "Warrior":  "\"Steel and will — that is all I need.\"",
            "Mage":     "\"The arcane bends to my command.\"",
            "Rogue":    "\"Shadows are my oldest friend.\"",
            "Paladin":  "\"Light guides every strike.\"",
            "Ranger":   "\"The wilds whisper my name.\"",
        }
        self.flavor_lbl.setText(flavors.get(cls, "\"Legend awaits.\""))
        self.show_status(f"✔  Character sheet generated for {name}.", color=GREEN_OK)

    def save_sheet(self):
        name = self.name_edit.text().strip() or "Unknown Hero"
        race = self.race_combo.currentText()
        cls  = self.class_combo.currentText()
        gender = self.gender_combo.currentText()

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Character Sheet", f"{name.replace(' ','_')}.txt",
            "Text Files (*.txt)"
        )
        if not path:
            self.show_status("Save cancelled.", color=MUTED)
            return

        lines = [
            "=" * 40,
            f"  CHARACTER SHEET",
            "=" * 40,
            f"  Name   : {name}",
            f"  Race   : {race}",
            f"  Class  : {cls}",
            f"  Gender : {gender}",
            "-" * 40,
            "  STATS",
            "-" * 40,
        ]
        for stat, row in self.stat_rows.items():
            v = row.value()
            bar = "█" * v + "░" * (20 - v)
            lines.append(f"  {stat}  [{bar}] {v:2d}")
        lines += [
            "-" * 40,
            f"  Total  : {self._total_points()} / {MAX_POINTS}",
            "=" * 40,
        ]

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        self.show_status(f"💾  Sheet saved to {path}", color=ACCENT2)


# ── entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG_LEFT))
    palette.setColor(QPalette.WindowText, QColor(TEXT_DARK))
    palette.setColor(QPalette.Base, QColor("#ffffff"))
    palette.setColor(QPalette.Highlight, QColor(ACCENT))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    win = CharacterBuilder()
    win.show()
    sys.exit(app.exec())