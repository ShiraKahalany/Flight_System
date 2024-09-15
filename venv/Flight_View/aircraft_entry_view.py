from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton

class AircraftEntryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout()

        self.manufacturer_input = QLineEdit(self)
        self.manufacturer_input.setPlaceholderText("Manufacturer")
        layout.addRow("Manufacturer:", self.manufacturer_input)

        self.nickname_input = QLineEdit(self)
        self.nickname_input.setPlaceholderText("Nickname")
        layout.addRow("Nickname:", self.nickname_input)

        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText("Year of Manufacture")
        layout.addRow("Year of Manufacture:", self.year_input)

        self.photo_input = QLineEdit(self)
        self.photo_input.setPlaceholderText("Photo URL")
        layout.addRow("Photo URL:", self.photo_input)

        self.submit_button = QPushButton("Submit", self)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
