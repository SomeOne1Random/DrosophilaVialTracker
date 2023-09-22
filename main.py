from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QLineEdit, QDateEdit, QComboBox
from PyQt6.QtCore import Qt, QDate
import sys
import json


class VialTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drosophila Melanogaster Vial Tracker')
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout()
        table_layout = QHBoxLayout()
        input_layout = QHBoxLayout()

        self.vial_table = QTableWidget()
        self.vial_table.setColumnCount(5)
        self.vial_table.setHorizontalHeaderLabels(['Color', 'Genotype', 'Temperature', 'New Vial Date', 'Flip Date'])
        table_layout.addWidget(self.vial_table)

        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText('Enter vial color')

        self.genotype_input = QLineEdit()
        self.genotype_input.setPlaceholderText('Enter genotype')

        self.temp_input = QComboBox()
        self.temp_input.addItems(['18', '21', '25', '29'])

        self.flip_date_input = QDateEdit()
        self.flip_date_input.setCalendarPopup(True)
        self.flip_date_input.setDate(QDate.currentDate())

        self.add_button = QPushButton('Add New Vial')
        self.add_button.clicked.connect(self.add_vial)

        self.flip_button = QPushButton('Add Flipped Vial')
        self.flip_button.clicked.connect(self.add_flipped_vial)

        self.update_button = QPushButton('Update Selected Vial')
        self.update_button.clicked.connect(self.update_vial)

        self.remove_button = QPushButton('Remove Selected Vial')
        self.remove_button.clicked.connect(self.remove_vial)

        self.save_exit_button = QPushButton('Save & Exit')
        self.save_exit_button.clicked.connect(self.save_and_exit)

        input_layout.addWidget(self.color_input)
        input_layout.addWidget(self.genotype_input)
        input_layout.addWidget(self.temp_input)
        input_layout.addWidget(self.flip_date_input)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.flip_button)
        input_layout.addWidget(self.update_button)
        input_layout.addWidget(self.remove_button)
        input_layout.addWidget(self.save_exit_button)

        main_layout.addLayout(table_layout)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)
        self.load_vials()

    def add_vial(self):
        self.add_vial_data(5)

    def add_flipped_vial(self):
        color = self.color_input.text()
        genotype = self.genotype_input.text()
        temperature = self.temp_input.currentText()
        flip_date = self.flip_date_input.date().toString(Qt.DateFormat.ISODate)

        if not (color and genotype):
            return

        row_position = self.vial_table.rowCount()
        self.vial_table.insertRow(row_position)

        self.vial_table.setItem(row_position, 0, QTableWidgetItem(color))
        self.vial_table.setItem(row_position, 1, QTableWidgetItem(genotype))
        self.vial_table.setItem(row_position, 2, QTableWidgetItem(temperature))
        self.vial_table.setItem(row_position, 3, QTableWidgetItem("Nothing"))  # Set to "Nothing"
        self.vial_table.setItem(row_position, 4, QTableWidgetItem(flip_date))

    def add_vial_data(self, days_to_add):
        color = self.color_input.text()
        genotype = self.genotype_input.text()
        temperature = self.temp_input.currentText()
        new_vial_date = self.flip_date_input.date().toString(Qt.DateFormat.ISODate)
        flip_date = (self.flip_date_input.date().addDays(days_to_add)).toString(Qt.DateFormat.ISODate)

        if not (color and genotype):
            return

        row_position = self.vial_table.rowCount()
        self.vial_table.insertRow(row_position)

        self.vial_table.setItem(row_position, 0, QTableWidgetItem(color))
        self.vial_table.setItem(row_position, 1, QTableWidgetItem(genotype))
        self.vial_table.setItem(row_position, 2, QTableWidgetItem(temperature))
        self.vial_table.setItem(row_position, 3, QTableWidgetItem(new_vial_date))
        self.vial_table.setItem(row_position, 4, QTableWidgetItem(flip_date))

    def update_vial(self):
        selected_row = self.vial_table.currentRow()
        if selected_row == -1:
            return
        color = self.color_input.text()
        genotype = self.genotype_input.text()
        temperature = self.temp_input.currentText()
        new_vial_date = self.flip_date_input.date().toString(Qt.DateFormat.ISODate)
        flip_date = (self.flip_date_input.date().addDays(5)).toString(Qt.DateFormat.ISODate)

        if not (color and genotype):
            return

        self.vial_table.setItem(selected_row, 0, QTableWidgetItem(color))
        self.vial_table.setItem(selected_row, 1, QTableWidgetItem(genotype))
        self.vial_table.setItem(selected_row, 2, QTableWidgetItem(temperature))
        self.vial_table.setItem(selected_row, 3, QTableWidgetItem(new_vial_date))
        self.vial_table.setItem(selected_row, 4, QTableWidgetItem(flip_date))

    def remove_vial(self):
        selected_row = self.vial_table.currentRow()
        if selected_row == -1:
            return
        self.vial_table.removeRow(selected_row)

    def save_and_exit(self):
        vial_data = []
        for row in range(self.vial_table.rowCount()):
            color = self.vial_table.item(row, 0).text()
            genotype = self.vial_table.item(row, 1).text()
            temperature = self.vial_table.item(row, 2).text()
            new_vial_date = self.vial_table.item(row, 3).text()
            flip_date = self.vial_table.item(row, 4).text()
            vial_data.append(
                {"color": color, "genotype": genotype, "temperature": temperature, "new_vial_date": new_vial_date,
                 "flip_date": flip_date})

        with open('vial_data.json', 'w') as f:
            json.dump(vial_data, f)
        self.close()

    def load_vials(self):
        try:
            with open('vial_data.json', 'r') as f:
                vial_data = json.load(f)
            for vial in vial_data:
                row_position = self.vial_table.rowCount()
                self.vial_table.insertRow(row_position)
                self.vial_table.setItem(row_position, 0, QTableWidgetItem(vial.get("color", "N/A")))
                self.vial_table.setItem(row_position, 1, QTableWidgetItem(vial.get("genotype", "N/A")))
                self.vial_table.setItem(row_position, 2, QTableWidgetItem(vial.get("temperature", "N/A")))
                self.vial_table.setItem(row_position, 3, QTableWidgetItem(vial.get("new_vial_date", "N/A")))
                self.vial_table.setItem(row_position, 4, QTableWidgetItem(vial.get("flip_date", "N/A")))
        except FileNotFoundError:
            pass


app = QApplication([])
window = VialTracker()
window.show()
sys.exit(app.exec())
