from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton
from mock_data import aircrafts

class AddAircraftView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.parent().go_back)
        layout.addWidget(self.back_button)

        # Create a form for adding new aircraft
        self.form_layout = QFormLayout()
        self.manufacturer_input = QLineEdit(self)
        self.nickname_input = QLineEdit(self)
        self.year_input = QLineEdit(self)
        self.image_url_input = QLineEdit(self)

        self.form_layout.addRow("Manufacturer", self.manufacturer_input)
        self.form_layout.addRow("Nickname", self.nickname_input)
        self.form_layout.addRow("Year of Manufacture", self.year_input)
        self.form_layout.addRow("Image URL", self.image_url_input)

        layout.addLayout(self.form_layout)

        # Submit button
        self.submit_button = QPushButton("Add Aircraft", self)
        self.submit_button.clicked.connect(self.add_aircraft)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_aircraft(self):
        # Logic to add a new aircraft to mock_data (simulated here)
        new_aircraft = {
            'id': len(aircrafts) + 1,
            'manufacturer': self.manufacturer_input.text(),
            'nickname': self.nickname_input.text(),
            'year_of_manufacture': int(self.year_input.text()),
            'image_url': self.image_url_input.text()
        }
        aircrafts.append(new_aircraft)
        print("New aircraft added:", new_aircraft)
