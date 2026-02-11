import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class BMICalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator")
        self.setFixedWidth(400)
        self.init_ui()

    def init_ui(self):
        # Main Layout container
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        # 1. Header
        header = QLabel("Adult and Child BMI Calculator")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            background-color: #B24C39; 
            color: white; 
            font-weight: bold; 
            padding: 8px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        """)
        main_layout.addWidget(header)

        # 2. Main Input Area Frame
        input_frame = QFrame()
        input_frame.setStyleSheet("background-color: #F4F4F4; border-left: 1px solid #CCC; border-right: 1px solid #CCC;")
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(20, 20, 20, 10)

        # Form Layout using Grid
        grid = QGridLayout()
        grid.setSpacing(10)

        # Calculate for:
        grid.addWidget(QLabel("Calculate BMI for:"), 0, 0)
        self.target_combo = QComboBox()
        self.target_combo.addItems(["Adult Age 20+", "Child/Teen Age 2-19"])
        grid.addWidget(self.target_combo, 0, 1, 1, 2)

        # Weight:
        grid.addWidget(QLabel("Weight:"), 1, 0)
        self.weight_input = QLineEdit()
        grid.addWidget(self.weight_input, 1, 1)
        self.weight_unit = QComboBox()
        self.weight_unit.addItems(["pounds", "kilograms"])
        grid.addWidget(self.weight_unit, 1, 2)

        # Height:
        grid.addWidget(QLabel("Height:"), 2, 0)
        self.height_ft_input = QLineEdit()
        grid.addWidget(self.height_ft_input, 2, 1)
        self.height_unit = QComboBox()
        self.height_unit.addItems(["feet", "meters", "centimeters"])
        grid.addWidget(self.height_unit, 2, 2)

        # Inches (Second height row)
        self.height_in_input = QLineEdit()
        grid.addWidget(self.height_in_input, 3, 1)
        grid.addWidget(QLabel("inches"), 3, 2)

        input_layout.addLayout(grid)

        # Buttons
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear")
        calc_btn = QPushButton("Calculate")
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(calc_btn)
        input_layout.addLayout(btn_layout)

        main_layout.addWidget(input_frame)

        # 3. Answer/Results Section
        answer_frame = QFrame()
        answer_frame.setStyleSheet("background-color: white; border: 1px solid #CCC; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;")
        answer_layout = QVBoxLayout(answer_frame)

        answer_label = QLabel("Answer:")
        answer_label.setStyleSheet("color: #666; border: none;")
        answer_layout.addWidget(answer_label)

        bmi_label = QLabel("BMI =")
        bmi_label.setAlignment(Qt.AlignCenter)
        bmi_label.setFont(QFont("Arial", 10, QFont.Bold))
        bmi_label.setStyleSheet("border: none;")
        answer_layout.addWidget(bmi_label)

        adult_bmi_header = QLabel("Adult BMI")
        adult_bmi_header.setAlignment(Qt.AlignCenter)
        adult_bmi_header.setStyleSheet("border: none; font-weight: bold;")
        answer_layout.addWidget(adult_bmi_header)

        # BMI Table
        self.table = QTableWidget(4, 2)
        self.table.setHorizontalHeaderLabels(["BMI", "Status"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setFixedHeight(150)

        # Table Content
        data = [
            ("≤ 18.4", "Underweight", "#FDE089"),
            ("18.5 - 24.9", "Normal", "#82CA7D"),
            ("25.0 - 39.9", "Overweight", "#F9A852"),
            ("≥ 40.0", "Obese", "#FF6666")
        ]

        for i, (bmi, status, color) in enumerate(data):
            bmi_item = QTableWidgetItem(bmi)
            bmi_item.setBackground(QColor(color))
            bmi_item.setTextAlignment(Qt.AlignCenter)
            
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)
            
            self.table.setItem(i, 0, bmi_item)
            self.table.setItem(i, 1, status_item)

        answer_layout.addWidget(self.table)
        main_layout.addWidget(answer_frame)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BMICalculator()
    window.show()
    sys.exit(app.exec())