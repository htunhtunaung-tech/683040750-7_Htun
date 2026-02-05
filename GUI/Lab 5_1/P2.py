import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QDateEdit,
    QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout,
    QComboBox, QTextEdit, QCheckBox, QPushButton
)
from PySide6.QtCore import QDate, Qt


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2: Student Registration")
        self.setFixedSize(400, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Student Registration Form")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        #layout.addSpacing(15)

        # Full Name
        layout.addWidget(QLabel("Full Name:"))
        layout.addWidget(QLineEdit())
        #layout.addSpacing(15)

        # Email
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(QLineEdit())
        #layout.addSpacing(15)

        # Phone
        layout.addWidget(QLabel("Phone:"))
        layout.addWidget(QLineEdit())
        #layout.addSpacing(15)

        # Date of Birth
        layout.addWidget(QLabel("Date of Birth (dd/MM/yyyy):"))
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDisplayFormat("dd/MM/yyyy")
        date_edit.setDate(QDate(2000, 1, 1))
        layout.addWidget(date_edit)
        #layout.addSpacing(15)

        # Gender
        layout.addWidget(QLabel("Gender:"))
        gender_layout = QHBoxLayout()

        gender_group = QButtonGroup(self)
        male_radio = QRadioButton("Male")
        female_radio = QRadioButton("Female")
        nonbinary_radio = QRadioButton("Non-binary")
        prefer_radio = QRadioButton("Prefer not to say")

        for r in [male_radio, female_radio, nonbinary_radio, prefer_radio]:
            gender_group.addButton(r)
            gender_layout.addWidget(r)

        layout.addLayout(gender_layout)
        #layout.addSpacing(15)

        # Program
        layout.addWidget(QLabel("Program:"))
        program_combo = QComboBox()
        program_combo.addItem("Select your program")
        program_combo.addItems([
            "Computer Engineering",
            "Digital Media Engineering",
            "Environmental Engineering",
            "Electical Engineering",
            "Semiconductor Engineering",
            "Mechanical Engineering",
            "Industrial Engineering",
            "Logistic Engineering",
            "Power Engineering",
            "Electronic Engineering",
            "Telecommunication Engineering",
            "Agricultural Engineering",
            "Civil Engineering",
            "ARIS"
        ])
        layout.addWidget(program_combo)
        #layout.addSpacing(15)

        # About yourself
        layout.addWidget(QLabel("Tell us a little bit about yourself:"))
        about_text = QTextEdit()
        about_text.setMaximumHeight(100)
        layout.addWidget(about_text)
        #layout.addSpacing(20)

        # Terms
        terms = QCheckBox("I accept the terms and conditions.")
        layout.addWidget(terms)
        #layout.addSpacing(20)

        # Submit button
        submit_btn = QPushButton("Submit Registration")
        layout.addWidget(submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(submit_btn)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec())
