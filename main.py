from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QLineEdit, QDateEdit, QComboBox, QLabel, QSpinBox
from PyQt6.QtCore import Qt, QDate
import sys
import json

class VialTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drosophila Melanogaster Vial Tracker')
        self.setGeometry(100, 100, 1700, 800)

        main_layout = QVBoxLayout()
        table_layout = QHBoxLayout()
        input_layout = QHBoxLayout()

        self.vial_table = QTableWidget()
        self.vial_table.setColumnCount(6)
        self.vial_table.setHorizontalHeaderLabels(
            ['Color', 'Genotype', 'Temperature', 'New Vial Date', 'Flip Date', 'Virgin Collection'])
        table_layout.addWidget(self.vial_table)

        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText('Enter vial color')

        self.genotype_input = QLineEdit()
        self.genotype_input.setPlaceholderText('Enter genotype')

        self.temp_input = QComboBox()
        self.temp_input.addItems(['18', '21', '25', '29'])

        new_vial_date_label = QLabel("New Vial Date:")
        self.new_vial_date_input = QDateEdit()
        self.new_vial_date_input.setCalendarPopup(True)
        self.new_vial_date_input.setDate(QDate.currentDate())

        flip_date_label = QLabel("Flip Date:")
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

        self.vial_count_spinbox = QSpinBox()
        self.vial_count_spinbox.setRange(1, 100)  # Let's say a max of 100 vials can be added at once
        self.vial_count_spinbox.setValue(1)  # Default to 1 vial
        self.vial_count_spinbox.setPrefix("Add ")
        self.vial_count_spinbox.setSuffix(" vials")

        self.vial_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.vial_table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)

        input_layout.addWidget(self.color_input)
        input_layout.addWidget(self.genotype_input)
        input_layout.addWidget(self.temp_input)
        input_layout.addWidget(new_vial_date_label)
        input_layout.addWidget(self.new_vial_date_input)
        input_layout.addWidget(flip_date_label)
        input_layout.addWidget(self.flip_date_input)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.flip_button)
        input_layout.addWidget(self.vial_count_spinbox)
        input_layout.addWidget(self.update_button)
        input_layout.addWidget(self.remove_button)
        input_layout.addWidget(self.save_exit_button)

        main_layout.addLayout(table_layout)
        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)
        self.load_vials()

    def get_selected_rows(self):
        selected_indexes = self.vial_table.selectedIndexes()
        return sorted(set(index.row() for index in selected_indexes))

    def add_vial(self):
        vial_count = self.vial_count_spinbox.value()  # Get the number of vials to add

        color = self.color_input.text()
        genotype = self.genotype_input.text()
        temperature = self.temp_input.currentText()
        new_vial_date = self.new_vial_date_input.date().toString(Qt.DateFormat.ISODate)
        flip_date = (self.new_vial_date_input.date().addDays(5)).toString(Qt.DateFormat.ISODate)
        virgin_collection = (self.new_vial_date_input.date().addDays(10)).toString(Qt.DateFormat.ISODate)

        if not (color and genotype):
            return

        for _ in range(vial_count):  # Loop to add the specified number of vials
            row_position = self.vial_table.rowCount()
            self.vial_table.insertRow(row_position)

            self.vial_table.setItem(row_position, 0, QTableWidgetItem(color))
            self.vial_table.setItem(row_position, 1, QTableWidgetItem(genotype))
            self.vial_table.setItem(row_position, 2, QTableWidgetItem(temperature))
            self.vial_table.setItem(row_position, 3, QTableWidgetItem(new_vial_date))
            self.vial_table.setItem(row_position, 4, QTableWidgetItem(flip_date))
            self.vial_table.setItem(row_position, 5, QTableWidgetItem(virgin_collection))

    def add_flipped_vial(self):
        vial_count = self.vial_count_spinbox.value()  # Get the number of flipped vials to add

        color = self.color_input.text()
        genotype = self.genotype_input.text()
        temperature = self.temp_input.currentText()
        flip_date = self.flip_date_input.date().toString(Qt.DateFormat.ISODate)
        virgin_collection = (self.flip_date_input.date().addDays(5)).toString(Qt.DateFormat.ISODate)

        if not (color and genotype):
            return

        for _ in range(vial_count):  # Loop to add the specified number of flipped vials
            row_position = self.vial_table.rowCount()
            self.vial_table.insertRow(row_position)

            self.vial_table.setItem(row_position, 0, QTableWidgetItem(color))
            self.vial_table.setItem(row_position, 1, QTableWidgetItem(genotype))
            self.vial_table.setItem(row_position, 2, QTableWidgetItem(temperature))
            self.vial_table.setItem(row_position, 3, QTableWidgetItem("Nothing"))  # Set to "Nothing"
            self.vial_table.setItem(row_position, 4, QTableWidgetItem(flip_date))
            self.vial_table.setItem(row_position, 5, QTableWidgetItem(virgin_collection))

    def update_vial(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            return

        color = self.color_input.text()
        genotype = self.genotype_input.text()
        temperature = self.temp_input.currentText()
        new_vial_date = self.new_vial_date_input.date().toString(Qt.DateFormat.ISODate)
        flip_date = (self.flip_date_input.date()).toString(Qt.DateFormat.ISODate)
        virgin_collection = (self.flip_date_input.date().addDays(5)).toString(Qt.DateFormat.ISODate)

        if not (color and genotype):
            return

        for row in selected_rows:
            self.vial_table.setItem(row, 0, QTableWidgetItem(color))
            self.vial_table.setItem(row, 1, QTableWidgetItem(genotype))
            self.vial_table.setItem(row, 2, QTableWidgetItem(temperature))
            self.vial_table.setItem(row, 3, QTableWidgetItem(new_vial_date))
            self.vial_table.setItem(row, 4, QTableWidgetItem(flip_date))
            self.vial_table.setItem(row, 5, QTableWidgetItem(virgin_collection))

    def remove_vial(self):
        selected_rows = self.get_selected_rows()
        for row in sorted(selected_rows, reverse=True):  # Remove from the last row to keep indexes consistent
            self.vial_table.removeRow(row)

    def save_and_exit(self):
        vial_data = []
        for row in range(self.vial_table.rowCount()):
            color = self.vial_table.item(row, 0).text()
            genotype = self.vial_table.item(row, 1).text()
            temperature = self.vial_table.item(row, 2).text()
            new_vial_date = self.vial_table.item(row, 3).text()
            flip_date = self.vial_table.item(row, 4).text()
            virgin_collection = self.vial_table.item(row, 5).text()
            vial_data.append(
                {"color": color, "genotype": genotype, "temperature": temperature, "new_vial_date": new_vial_date,
                 "flip_date": flip_date, "virgin_collection": virgin_collection})

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
                self.vial_table.setItem(row_position, 5, QTableWidgetItem(vial.get("virgin_collection", "N/A")))
        except FileNotFoundError:
            pass


app = QApplication([])
window = VialTracker()
window.show()
sys.exit(app.exec())
