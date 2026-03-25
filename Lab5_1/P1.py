"""
Htun Htun Aung
683040750-7
P1
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QCheckBox, QVBoxLayout, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt

class LoginUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login UI")
        self.setFixedSize(350, 520)
        self.setStyleSheet("background-color: #f9f9f9;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(40, 30, 40, 30)

        # ===== Title =====
        title = QLabel("LOGIN")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        main_layout.addWidget(title)

        # ===== Email =====
        email_label = QLabel("Email")
        email_input = QLineEdit()
        email_input.setFixedHeight(35)
        email_input.setStyleSheet("border: 1px solid #ddd; border-radius: 4px; padding-left: 5px; background: white;")
        main_layout.addWidget(email_label)
        main_layout.addWidget(email_input)

        # ===== Password =====
        password_label = QLabel("Password")
        password_input = QLineEdit()
        password_input.setFixedHeight(35)
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet("border: 1px solid #ddd; border-radius: 4px; padding-left: 5px; background: white;")
        main_layout.addWidget(password_label)
        main_layout.addWidget(password_input)

        # ===== Remember me (FIXED WHITE MARK HERE) =====
        remember_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Remember me?")
        
        # This CSS creates the pink box and the white tick
        self.remember_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #f45b85;
                border: 1px solid #f45b85;
                /* This is the white checkmark icon encoded as an SVG */
                image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'><path d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/></svg>");
            }
        """)

        remember_layout.addWidget(self.remember_checkbox)
        remember_layout.addStretch()
        main_layout.addLayout(remember_layout)

        # ===== Login Button =====
        login_btn = QPushButton("LOGIN")
        login_btn.setFixedHeight(40)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #f45b85;
                color: white;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e04a74;
            }
        """)
        main_layout.addWidget(login_btn)

        # ===== Forgot Password =====
        forgot_label = QLabel("Forgot Password?")
        forgot_label.setAlignment(Qt.AlignRight)
        forgot_label.setStyleSheet("color: gray; font-size: 11px;")
        main_layout.addWidget(forgot_label)

        # ===== OR Divider =====
        divider_layout = QHBoxLayout()
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet("color: #ddd;")
        
        or_label = QLabel("OR")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setFixedWidth(40)
        or_label.setStyleSheet("border: 1px solid #ddd; border-radius: 10px; background: white; color: gray;")

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("color: #ddd;")

        divider_layout.addWidget(line1)
        divider_layout.addWidget(or_label)
        divider_layout.addWidget(line2)
        main_layout.addLayout(divider_layout)

        # ===== Social Buttons =====
        social_layout = QHBoxLayout()
        social_layout.setSpacing(20)
        social_layout.setAlignment(Qt.AlignCenter)

        def get_social_style(color):
            return f"border: 2px solid {color}; color: {color}; border-radius: 20px; font-weight: bold; font-size: 16px; background: white;"

        google_btn = QPushButton("G")
        google_btn.setStyleSheet(get_social_style("#DB4437"))
        fb_btn = QPushButton("f")
        fb_btn.setStyleSheet(get_social_style("#4267B2"))
        in_btn = QPushButton("in")
        in_btn.setStyleSheet(get_social_style("#0A66C2"))

        for btn in (google_btn, fb_btn, in_btn):
            btn.setFixedSize(40, 40)
            social_layout.addWidget(btn)

        main_layout.addLayout(social_layout)

        # ===== Sign Up =====
        signup_layout = QHBoxLayout()
        signup_layout.setAlignment(Qt.AlignCenter)
        need_label = QLabel("Need an account?")
        signup_label = QLabel("SIGN UP")
        signup_label.setStyleSheet("font-weight: bold; text-decoration: underline;")
        signup_layout.addWidget(need_label)
        signup_layout.addWidget(signup_label)
        main_layout.addLayout(signup_layout)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginUI()
    window.show()
    sys.exit(app.exec())