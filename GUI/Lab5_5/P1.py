"""
Htun Htun Aung
683040750-7
P1 Lab5_5
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QSpinBox,
    QPushButton, QDialog, QMessageBox, QScrollArea,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont, QIntValidator, QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression


class RoomCard(QWidget):
    room_selected = Signal(str, int)

    def __init__(self, room_name: str, price: int, description: str, emoji: str = "🏨", max_guests: int = 1):
        super().__init__()
        self._is_selected = False
        self._room_name = room_name
        self._price = price
        self._max_guests = max_guests

        self._build_ui(room_name, price, emoji, description, max_guests)
        self.deselect()

    def _build_ui(self, room_name: str, price: int, emoji: str, description: str, max_guests: int):
        self.setFixedSize(170, 200)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        emoji_lbl = QLabel(emoji)
        emoji_lbl.setFont(QFont("Segoe UI", 28))
        emoji_lbl.setAlignment(Qt.AlignCenter)

        name_lbl = QLabel(room_name)
        name_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setStyleSheet("color: #1e1b4b;")

        price_lbl = QLabel(f"${price} / night")
        price_lbl.setFont(QFont("Segoe UI", 10))
        price_lbl.setAlignment(Qt.AlignCenter)
        price_lbl.setStyleSheet("color: #6366f1; font-weight: bold;")

        desc_lbl = QLabel(description)
        desc_lbl.setFont(QFont("Segoe UI", 8))
        desc_lbl.setAlignment(Qt.AlignCenter)
        desc_lbl.setStyleSheet("color: #6b7280;")
        desc_lbl.setWordWrap(True)

        capacity_lbl = QLabel(f"👤 Max {max_guests} guest(s)")
        capacity_lbl.setFont(QFont("Segoe UI", 8))
        capacity_lbl.setAlignment(Qt.AlignCenter)
        capacity_lbl.setStyleSheet("color: #ef4444; font-weight: bold;")

        self.select_btn = QPushButton("Select Room")
        self.select_btn.setFixedHeight(30)
        self.select_btn.setCursor(Qt.PointingHandCursor)
        self.select_btn.clicked.connect(self._on_select_clicked)

        layout.addWidget(emoji_lbl)
        layout.addWidget(name_lbl)
        layout.addWidget(price_lbl)
        layout.addWidget(desc_lbl)
        layout.addWidget(capacity_lbl)
        layout.addStretch()
        layout.addWidget(self.select_btn)

    def _on_select_clicked(self):
        self.room_selected.emit(self._room_name, self._price)

    def select(self):
        self._is_selected = True
        self.setStyleSheet("""
            RoomCard {
                background-color: #f0fdf4;
                border: 2px solid #22c55e;
                border-radius: 12px;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.select_btn.setText("✓ Selected")

    def deselect(self):
        self._is_selected = False
        self.setStyleSheet("""
            RoomCard {
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 12px;
            }
            RoomCard:hover {
                border: 2px solid #6366f1;
                background-color: #f5f3ff;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        self.select_btn.setText("Select Room")

    def is_selected(self):
        return self._is_selected


class ConfirmDialog(QDialog):
    def __init__(self, guest_name: str, room_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmed")
        self.setFixedSize(360, 250)
        self.setModal(True)
        self._build_ui(guest_name, room_name)

    def _build_ui(self, guest_name: str, room_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        check_lbl = QLabel("✔")
        check_lbl.setFont(QFont("Segoe UI", 22, QFont.Bold))
        check_lbl.setAlignment(Qt.AlignCenter)
        check_lbl.setStyleSheet("""
            background-color: #22c55e;
            border-radius: 4px;
            color: white;
        """)
        check_lbl.setFixedSize(50, 38)

        icon_layout = QHBoxLayout()
        icon_layout.addStretch()
        icon_layout.addWidget(check_lbl)
        icon_layout.addStretch()

        title_lbl = QLabel("Booking Successful!")
        title_lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("color: #16a34a;")

        msg_lbl = QLabel(f"Dear {guest_name},\n{room_name} is ready to welcome you! 🎉")
        msg_lbl.setFont(QFont("Segoe UI", 10))
        msg_lbl.setAlignment(Qt.AlignCenter)
        msg_lbl.setStyleSheet("color: #374151;")

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(44)
        ok_btn.setMinimumWidth(280)
        ok_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #16a34a; }
        """)
        ok_btn.clicked.connect(self.accept)

        layout.addLayout(icon_layout)
        layout.addWidget(title_lbl)
        layout.addWidget(msg_lbl)
        layout.addStretch()
        layout.addWidget(ok_btn)


class BookingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_room = None
        self.selected_price = 0
        self.selected_max_guests = 0
        self.cards = []
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(20)

        title = QLabel("🏨 Book Your Stay at CozyStay")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")

        subtitle = QLabel("Fill in your details and choose your room")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        form_title = QLabel("📋 Guest Information")
        form_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        form_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(form_title)

        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 10px;
            }
        """)

        # Input widgets
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Louis Htun")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("e.g. 081-234-5678")
        self.phone_input.textChanged.connect(self._format_phone)

        self.checkin_input = QDateEdit()
        self.checkin_input.setDate(QDate.currentDate())
        self.checkin_input.setDisplayFormat("dd/MM/yyyy")
        self.checkin_input.setCalendarPopup(True)

        self.checkout_input = QDateEdit()
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.checkout_input.setDisplayFormat("dd/MM/yyyy")
        self.checkout_input.setCalendarPopup(True)

        self.guests_input = QSpinBox()
        self.guests_input.setMinimum(1)
        self.guests_input.setMaximum(10)
        self.guests_input.setValue(1)
        self.guests_input.setSuffix(" guest(s)")

        input_style = """
            QLineEdit, QDateEdit, QSpinBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus, QDateEdit:focus, QSpinBox:focus {
                border: 1px solid #6366f1;
            }
        """
        for w in [self.name_input, self.phone_input,
                  self.checkin_input, self.checkout_input, self.guests_input]:
            w.setStyleSheet(input_style)
            w.setMinimumWidth(200)

        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(20, 16, 20, 16)
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)

        label_style = "font-size: 13px; color: #374151; font-weight: bold;"
        for text, widget in [
            ("Full Name :",       self.name_input),
            ("Phone Number :",    self.phone_input),
            ("Check-in Date :",   self.checkin_input),
            ("Check-out Date :",  self.checkout_input),
            ("Guests :",          self.guests_input),
        ]:
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            form_layout.addRow(lbl, widget)

        main_layout.addWidget(form_frame)

        # Room selection
        room_title = QLabel("🛏 Select a Room")
        room_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        room_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(room_title)

        rooms_data = [
            ("Standard Room", 50,  "Single bed, Free Wi-Fi",             "🛏",  1),
            ("Deluxe Room",   120, "Double bed, Ocean view, Wi-Fi",      "🌊",  2),
            ("Suite Room",    250, "Living room, Jacuzzi, Premium view", "👑",  4),
            ("Family Room",   160, "2 Bedrooms, Perfect for families",   "👨‍👩‍👧‍👦", 6),
        ]

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        for room_name, price, description, emoji, max_guests in rooms_data:
            card = RoomCard(room_name, price, description, emoji, max_guests)
            card.room_selected.connect(self._on_room_selected)
            self.cards.append(card)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        main_layout.addLayout(cards_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.clear_btn = QPushButton("🗑  Clear Info")
        self.clear_btn.setFixedHeight(42)
        self.clear_btn.setFont(QFont("Segoe UI", 11))
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)
        self.clear_btn.clicked.connect(self.clear_form)

        self.next_btn = QPushButton("Next →")
        self.next_btn.setFixedHeight(42)
        self.next_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        scroll.setWidget(container)

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)

    def _format_phone(self, text: str):
        """Auto-format phone number as XXX-XXX-XXXX while typing"""
        digits = "".join(filter(str.isdigit, text))
        digits = digits[:10]
        if len(digits) <= 3:
            formatted = digits
        elif len(digits) <= 6:
            formatted = f"{digits[:3]}-{digits[3:]}"
        else:
            formatted = f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        self.phone_input.blockSignals(True)
        self.phone_input.setText(formatted)
        self.phone_input.setCursorPosition(len(formatted))
        self.phone_input.blockSignals(False)

    def _on_room_selected(self, room_name: str, price: int):
        self.selected_room = room_name
        self.selected_price = price
        for card in self.cards:
            if card._room_name == room_name:
                self.selected_max_guests = card._max_guests
                card.select()
            else:
                card.deselect()

    def clear_form(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.checkin_input.setDate(QDate.currentDate())
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.guests_input.setValue(1)
        self.selected_room = None
        self.selected_price = 0
        self.selected_max_guests = 0
        for card in self.cards:
            card.deselect()

    def get_booking_data(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        checkin = self.checkin_input.date()
        checkout = self.checkout_input.date()

        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter your full name.")
            return None
        if not phone:
            QMessageBox.warning(self, "Missing Information", "Please enter your phone number.")
            return None
        if checkin >= checkout:
            QMessageBox.warning(self, "Invalid Dates",
                                "Check-out date must be after check-in date.")
            return None
        if not self.selected_room:
            QMessageBox.warning(self, "No Room Selected",
                                "Please select a room before proceeding.")
            return None

        guests = self.guests_input.value()
        if guests > self.selected_max_guests:
            QMessageBox.warning(
                self, "Too Many Guests",
                f"'{self.selected_room}' allows a maximum of {self.selected_max_guests} guest(s).\n"
                f"You selected {guests} guest(s). Please reduce the number of guests or choose a different room."
            )
            return None

        nights = checkin.daysTo(checkout)
        total = self.selected_price * nights

        data_dict = {
            "room": self.selected_room,
            "price": self.selected_price,
            "name": name,
            "phone": phone,
            "checkin": checkin.toString("dd/MM/yyyy"),
            "checkout": checkout.toString("dd/MM/yyyy"),
            "nights": nights,
            "guests": self.guests_input.value(),
            "total": total,
        }
        return data_dict


class ReviewPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_data = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(16)

        title = QLabel("📋 Booking Summary")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")

        subtitle = QLabel("Please review your details before confirming")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 12px;
            }
        """)

        self.info_layout = QGridLayout(self.info_frame)
        self.info_layout.setContentsMargins(24, 20, 24, 20)
        self.info_layout.setSpacing(10)
        self.info_layout.setColumnStretch(1, 1)

        key_style = "font-weight: bold; color: #374151; font-size: 13px;"
        val_style = "color: #1f2937; font-size: 13px;"

        display_data = [
            ("🛏  Room",            "—"),
            ("💰  Price / Night",   "$—"),
            ("👤  Guest Name",      "—"),
            ("📞  Phone",           "—"),
            ("📅  Check-in",        "—"),
            ("📅  Check-out",       "—"),
            ("🌙  Nights",          "— night(s)"),
            ("👥  Guests",          "— guest(s)"),
        ]

        self.val_labels = []
        for row, (key, val) in enumerate(display_data):
            k_lbl = QLabel(key)
            k_lbl.setStyleSheet(key_style)
            v_lbl = QLabel(val)
            v_lbl.setStyleSheet(val_style)
            self.val_labels.append(v_lbl)
            self.info_layout.addWidget(k_lbl, row, 0)
            self.info_layout.addWidget(v_lbl, row, 1)

        layout.addWidget(self.info_frame)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #e5e7eb;")
        layout.addWidget(line)

        total_layout = QHBoxLayout()
        total_layout.addStretch()

        total_icon = QLabel("💳")
        total_icon.setFont(QFont("Segoe UI", 14))

        self.total_lbl = QLabel("Total Amount: $—")
        self.total_lbl.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.total_lbl.setStyleSheet("color: #6366f1;")

        total_layout.addWidget(total_icon)
        total_layout.addWidget(self.total_lbl)
        layout.addLayout(total_layout)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.back_btn = QPushButton("←  Back")
        self.back_btn.setFixedHeight(44)
        self.back_btn.setFont(QFont("Segoe UI", 11))
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 22px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)

        self.submit_btn = QPushButton("✅  Confirm Booking")
        self.submit_btn.setFixedHeight(44)
        self.submit_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #16a34a; }
        """)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        layout.addLayout(btn_layout)

    def load_data(self, data: dict):
        self.current_data = data
        values = [
            data.get("room", "—"),
            f"${data.get('price', '—')}",
            data.get("name", "—"),
            data.get("phone", "—"),
            data.get("checkin", "—"),
            data.get("checkout", "—"),
            f"{data.get('nights', '—')} night(s)",
            f"{data.get('guests', '—')} guest(s)",
        ]
        for lbl, val in zip(self.val_labels, values):
            lbl.setText(str(val))
        self.total_lbl.setText(f"Total Amount: ${data.get('total', '—')}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CozyStay — Hotel Booking System")
        self.setMinimumSize(820, 680)
        self.resize(900, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.booking_page = BookingPage()
        self.review_page = ReviewPage()

        self.stack.addWidget(self.booking_page)   # index 0
        self.stack.addWidget(self.review_page)    # index 1

        self.booking_page.next_btn.clicked.connect(self._go_to_review)
        self.review_page.back_btn.clicked.connect(self._go_to_booking)
        self.review_page.submit_btn.clicked.connect(self._on_submit)

        self.stack.setCurrentIndex(0)

        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0ff; }
            QScrollArea  { background-color: transparent; }
            QWidget      { font-family: 'Segoe UI', 'Tahoma', sans-serif; }
        """)

    def _go_to_review(self):
        data = self.booking_page.get_booking_data()
        if data is None:
            return
        self.review_page.load_data(data)
        self.stack.setCurrentIndex(1)

    def _go_to_booking(self):
        self.stack.setCurrentIndex(0)

    def _on_submit(self):
        data = self.review_page.current_data
        dlg = ConfirmDialog(data.get("name", "Guest"), data.get("room", "Room"), self)
        dlg.exec()
        self.booking_page.clear_form()
        self.stack.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()