from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QLineEdit, QPushButton

class FlightEntryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout()

        self.aircraft_dropdown = QComboBox(self)
        # Populate dropdown with aircraft from the system
        layout.addRow("Aircraft:", self.aircraft_dropdown)

        self.source_input = QLineEdit(self)
        layout.addRow("Source:", self.source_input)

        self.destination_input = QLineEdit(self)
        layout.addRow("Destination:", self.destination_input)

        self.departure_input = QLineEdit(self)
        layout.addRow("Departure Date and Time:", self.departure_input)

        self.landing_input = QLineEdit(self)
        layout.addRow("Estimated Landing Date and Time:", self.landing_input)

        self.submit_button = QPushButton("Submit", self)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
