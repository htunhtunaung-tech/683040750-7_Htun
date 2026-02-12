import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QWidget, QLabel, QLineEdit, QPushButton, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Constants
kg, lb = "kilograms", "pounds"
cm, m, ft, inch = "centimeters", "meters", "feet", "inches"
adult = "Adults 20+"
child = "Children and Teenagers (5-19)"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: BMI Calculator")
        self.setFixedWidth(350)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header
        header = QLabel("Adult and Child BMI Calculator")
        header.setStyleSheet("background-color: brown; color: white; font-weight: bold; padding: 5px;")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Sections
        self.output_section = OutputSection()
        self.input_section = InputSection(self.output_section)
        
        main_layout.addLayout(self.input_section)

        # Result Container (Linen Background)
        result_container = QWidget()
        result_container.setStyleSheet("background-color: #FAF0E6;")
        result_container.setLayout(self.output_section)
        main_layout.addWidget(result_container)

class OutputSection(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignTop)
        
        self.bmi_title = QLabel("Your BMI")
        self.bmi_title.setAlignment(Qt.AlignCenter)
        
        self.bmi_value = QLabel("0.00")
        self.bmi_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.bmi_value.setStyleSheet("color: blue;")
        self.bmi_value.setAlignment(Qt.AlignCenter)
        
        self.addWidget(self.bmi_title)
        self.addWidget(self.bmi_value)
        
        # Placeholder for dynamic content (Table or Links)
        self.dynamic_widget = QWidget()
        self.dynamic_layout = QVBoxLayout(self.dynamic_widget)
        self.addWidget(self.dynamic_widget)

    def update_results(self, bmi, age_group):
        self.bmi_value.setText(f"{bmi:.2f}")
        self.clear_dynamic_section()
        
        if age_group == adult:
            self.show_adult_table()
        else:
            self.show_child_link()

    def show_adult_table(self):
        grid = QGridLayout()
        headers = [("BMI", 0), ("Condition", 1)]
        rows = [("< 18.5", "Thin"), ("18.5 - 25.0", "Normal"), 
                ("25.1 - 30.0", "Overweight"), ("> 30.0", "Obese")]
        
        for text, col in headers:
            lbl = QLabel(text)
            lbl.setFont(QFont("Arial", 10, QFont.Bold))
            grid.addWidget(lbl, 0, col)
            
        for i, (val, cond) in enumerate(rows, 1):
            grid.addWidget(QLabel(val), i, 0)
            grid.addWidget(QLabel(cond), i, 1)
            
        self.dynamic_layout.addLayout(grid)

    def show_child_link(self):
        instr = QLabel("For child's BMI interpretation, please click one of the following links:")
        instr.setWordWrap(True)
        links = QHBoxLayout()
        boy = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-boys-z-5-19years.pdf">BMI graph for BOYS</a>')
        girl = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-girls-z-5-19years.pdf">BMI graph for GIRLS</a>')
        for link in [boy, girl]:
            link.setOpenExternalLinks(True)
            links.addWidget(link)
        
        self.dynamic_layout.addWidget(instr)
        self.dynamic_layout.addLayout(links)

    def clear_result(self):
        self.bmi_value.setText("0.00")
        self.clear_dynamic_section()

    def clear_dynamic_section(self):
        while self.dynamic_layout.count():
            item = self.dynamic_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            elif item.layout(): self.clear_layout(item.layout())

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

class InputSection(QVBoxLayout):
    def __init__(self, output_sec):
        super().__init__()
        self.output_sec = output_sec

        # Form Elements
        self.age_combo = QComboBox()
        self.age_combo.addItems([adult, child])
        
        self.weight_input = QLineEdit()
        self.weight_unit = QComboBox()
        self.weight_unit.addItems([kg, lb])
        
        self.height_input = QLineEdit()
        self.height_unit = QComboBox()
        self.height_unit.addItems([cm, m, inch])

        # Layouts
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("BMI age group:"))
        row1.addWidget(self.age_combo)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Weight:"))
        row2.addWidget(self.weight_input)
        row2.addWidget(self.weight_unit)
        
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Height:"))
        row3.addWidget(self.height_input)
        row3.addWidget(self.height_unit)

        self.addLayout(row1); self.addLayout(row2); self.addLayout(row3)

        # Buttons
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("clear")
        submit_btn = QPushButton("Submit Registration")
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(submit_btn)
        self.addLayout(btn_layout)

        # Signals
        clear_btn.clicked.connect(self.clear_form)
        submit_btn.clicked.connect(self.submit_reg)

    def clear_form(self):
        self.weight_input.clear()
        self.height_input.clear()
        self.output_sec.clear_result()

    def submit_reg(self):
        try:
            w = float(self.weight_input.text())
            h = float(self.height_input.text())
            w_u = self.weight_unit.currentText()
            h_u = self.height_unit.currentText()
            
            # Convert to Metric for standard formula
            if w_u == lb: w = w * 0.453592
            
            if h_u == cm: h = h / 100
            elif h_u == inch: h = h * 0.0254
            # if meters, h stays h
            
            bmi = w / (h * h)
            self.output_sec.update_results(bmi, self.age_combo.currentText())
        except (ValueError, ZeroDivisionError):
            pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()