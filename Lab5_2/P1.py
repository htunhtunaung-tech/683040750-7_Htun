"""
Htun Htun Aung
683040750-7
P1 Lab5_2
"""

import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

kg = "kilograms"
lb = "pounds"
cm = "centimeters"
ft = "feet"

adult = "Adults 20+"
child = "Children and Teenagers (5-19)"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: BMI Calculator")
        self.setFixedSize(360, 520)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Title
        title = QLabel("Adult and Child BMI Calculator")
        title.setStyleSheet("background-color:#8B1E1E;color:white;padding:8px;")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(title)

        # Sections
        self.output_section = OutputSection()
        self.input_section = InputSection(self.output_section)

        main_layout.addWidget(self.input_section)

        # Result container
        result_container = QWidget()
        result_container.setStyleSheet("background-color:#FAF0E6;")
        container_layout = QVBoxLayout(result_container)
        container_layout.addWidget(self.output_section)

        main_layout.addWidget(result_container)


class InputSection(QWidget):
    def __init__(self, output_section):
        super().__init__()
        self.output_section = output_section

        main_layout = QVBoxLayout(self)
        form = QFormLayout()

        # Age group
        self.age_combo = QComboBox()
        self.age_combo.addItems([adult, child])
        form.addRow("BMI age group:", self.age_combo)

        # Weight
        self.weight_edit = QLineEdit()
        self.weight_unit = QComboBox()
        self.weight_unit.addItems([kg, lb])
        w_layout = QHBoxLayout()
        w_layout.addWidget(self.weight_edit)
        w_layout.addWidget(self.weight_unit)
        form.addRow("Weight:", w_layout)

        # Height
        self.height_edit = QLineEdit()
        self.height_unit = QComboBox()
        self.height_unit.addItems([cm, ft])
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.height_edit)
        h_layout.addWidget(self.height_unit)
        form.addRow("Height:", h_layout)

        main_layout.addLayout(form)

        # Buttons
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("clear")
        submit_btn = QPushButton("Submit Registration")
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(submit_btn)
        main_layout.addLayout(btn_layout)

        clear_btn.clicked.connect(self.clear_form)
        submit_btn.clicked.connect(self.submit_reg)

    def calculate_BMI(self):
        weight = float(self.weight_edit.text())
        height = float(self.height_edit.text())

        if self.weight_unit.currentText() == lb:
            weight *= 0.453592

        if self.height_unit.currentText() == cm:
            height /= 100
        elif self.height_unit.currentText() == ft:
            height *= 0.3048

        bmi = weight / (height ** 2)
        return round(bmi, 2)

    def submit_reg(self):
        try:
            bmi = self.calculate_BMI()
            age_group = self.age_combo.currentText()
            self.output_section.update_results(bmi, age_group)
        except:
            QMessageBox.warning(self, "Error", "Please enter valid numbers!")

    def clear_form(self):
        self.weight_edit.clear()
        self.height_edit.clear()
        self.output_section.clear_result()


class OutputSection(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        self.label_title = QLabel("Your BMI")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setFont(QFont("Arial", 11))
        main_layout.addWidget(self.label_title)

        self.bmi_label = QLabel("0.00")
        self.bmi_label.setAlignment(Qt.AlignCenter)
        self.bmi_label.setFont(QFont("Arial", 26, QFont.Bold))
        self.bmi_label.setStyleSheet("color:#3A5AFF;")
        main_layout.addWidget(self.bmi_label)

        self.extra_layout = QVBoxLayout()
        main_layout.addLayout(self.extra_layout)

        main_layout.addStretch()

    def update_results(self, bmi, age_group):
        self.clear_extra()
        self.bmi_label.setText(f"{bmi:.2f}")

        if age_group == adult:
            self.show_adult_table()
        else:
            self.show_child_link()

    def show_adult_table(self):
        grid = QGridLayout()

        headers = ["BMI", "Condition"]
        for i, h in enumerate(headers):
            lbl = QLabel(h)
            lbl.setFont(QFont("Arial", 10, QFont.Bold))
            grid.addWidget(lbl, 0, i, Qt.AlignCenter)

        rows = [
            ("< 18.5", "Thin"),
            ("18.5 - 25.0", "Normal"),
            ("25.1 - 30.0", "Overweight"),
            ("> 30.0", "Obese"),
        ]

        for r, (b, c) in enumerate(rows, 1):
            grid.addWidget(QLabel(b), r, 0, Qt.AlignCenter)
            grid.addWidget(QLabel(c), r, 1, Qt.AlignCenter)

        self.extra_layout.addLayout(grid)

    def show_child_link(self):
        info = QLabel("For child's BMI interpretation, please click one of the following links.")
        info.setAlignment(Qt.AlignCenter)
        self.extra_layout.addWidget(info)

        link_layout = QHBoxLayout()
        boy = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-boys-z-5-19years.pdf">BMI graph for BOYS</a>')
        girl = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-girls-z-5-19years.pdf">BMI graph for GIRLS</a>')
        boy.setOpenExternalLinks(True)
        girl.setOpenExternalLinks(True)

        link_layout.addWidget(boy)
        link_layout.addWidget(girl)
        self.extra_layout.addLayout(link_layout)

    def clear_result(self):
        self.bmi_label.setText("0.00")
        self.clear_extra()

    def clear_extra(self):
        while self.extra_layout.count():
            item = self.extra_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
