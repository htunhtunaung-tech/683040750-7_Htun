# Name: Htun Htun Aung
# Student ID: [683040750-7]

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame,
)
from PySide6.QtCore import Qt, Signal, QMimeData, QPoint
from PySide6.QtGui import QFont, QCursor, QDrag, QPixmap

from style import C


class StudentCard(QFrame):

    # Signal for delete request: emits self
    delete_requested = Signal(object)

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data

        # for drag and drop
        self._drag_start: QPoint | None = None
        self.setAcceptDrops(False)
        self.setCursor(QCursor(Qt.OpenHandCursor))

        self._build()

    def _build(self):
        # collect non-empty courses
        courses = [
            v for key in ("course1", "course2", "course3")
            if (v := self.data.get(key, "")) and v != "— Select Course —"
        ]

        # base height: name + dept rows, plus 18px per course line
        self.setMinimumHeight(70 + len(courses) * 20)

        self.setStyleSheet(f"""
            QFrame {{
                background:{C['card']};
                border-radius:6px;
                margin:2px 0px;
            }}
            QFrame:hover {{
                background:{C['surface']};
            }}
        """)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.setSpacing(8)

        # drag handle
        handle = QLabel("⠿")
        handle.setFixedWidth(16)
        handle.setAlignment(Qt.AlignTop)
        handle.setStyleSheet(
            f"background:transparent; color:{C['muted']};font-size:18px;padding-top:2px;"
        )
        outer.addWidget(handle)

        # info area
        info = QVBoxLayout()
        info.setSpacing(2)

        # name + id row
        name_row = QHBoxLayout()
        name_row.setSpacing(8)
        fullname = f"{self.data.get('first_name', '')} {self.data.get('last_name', '')}".strip()
        self.data['fullname'] = fullname
        lbl_name = QLabel(f"<b>{fullname}</b>")
        lbl_name.setStyleSheet(f"color:{C['text']};font-size:13px;background:transparent;")
        lbl_id = QLabel(self.data.get("student_id", ""))
        lbl_id.setStyleSheet(f"color:{C['muted']};font-size:12px;background:transparent;")
        name_row.addWidget(lbl_name)
        name_row.addWidget(lbl_id)
        name_row.addStretch()
        info.addLayout(name_row)

        # faculty · major
        dept = f"{self.data.get('faculty', '')} · {self.data.get('major', '')}"
        lbl_dept = QLabel(dept)
        lbl_dept.setStyleSheet(f"color:{C['muted']};font-size:12px;background:transparent;")
        info.addWidget(lbl_dept)

        # courses
        for c in courses:
            lbl_c = QLabel(c)
            lbl_c.setStyleSheet(f"color:{C['text']};font-size:12px;background:transparent;")
            info.addWidget(lbl_c)

        outer.addLayout(info)
        outer.addStretch()

        # delete button
        btn_del = QPushButton("✕")
        btn_del.setFixedSize(28, 28)
        btn_del.setCursor(QCursor(Qt.PointingHandCursor))
        btn_del.setStyleSheet(f"""
            QPushButton {{
                background:transparent;
                color:{C['muted']};
                border:none;
                border-radius:14px;
                font-size:11px;
                font-weight:bold;
            }}
            QPushButton:hover {{
                background:{C['red']};
                color:white;
                border:none;
            }}
        """)
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))
        outer.addWidget(btn_del, alignment=Qt.AlignTop)

    # ── Drag support ──────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self._drag_start is not None:
            if (event.pos() - self._drag_start).manhattanLength() > 10:
                drag = QDrag(self)
                mime = QMimeData()
                mime.setText("student_card")
                drag.setMimeData(mime)

                pix = QPixmap(self.size())
                pix.fill(Qt.transparent)
                self.render(pix)
                drag.setPixmap(pix)
                drag.setHotSpot(event.pos())
                drag.exec(Qt.MoveAction)
        super().mouseMoveEvent(event)