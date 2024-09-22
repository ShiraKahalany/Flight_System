from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QDateTimeEdit
from datetime import datetime

class AddFlightView(QWidget):
    def __init__(self, controller, aircrafts):
        super().__init__()
        self.controller = controller
        self.aircrafts = aircrafts

        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.controller.go_back)
        layout.addWidget(self.back_button)

        # Create a form for adding new flights
        self.form_layout = QFormLayout()

        # Dropdown to select aircraft
        self.aircraft_dropdown = QComboBox(self)
        for aircraft in self.aircrafts:
            # Access Aircraft object attributes using dot notation
            self.aircraft_dropdown.addItem(f"{aircraft.nickname} ({aircraft.manufacturer})", aircraft.id)
        self.form_layout.addRow("Aircraft", self.aircraft_dropdown)

        # Source and destination input fields
        self.source_input = QLineEdit(self)
        self.form_layout.addRow("Source", self.source_input)

        self.destination_input = QLineEdit(self)
        self.form_layout.addRow("Destination", self.destination_input)

        # DateTime inputs for departure and landing
        self.departure_input = QDateTimeEdit(self)
        self.departure_input.setDateTime(datetime.now())
        self.departure_input.setCalendarPopup(True)
        self.form_layout.addRow("Departure Time", self.departure_input)

        self.landing_input = QDateTimeEdit(self)
        self.landing_input.setDateTime(datetime.now())
        self.landing_input.setCalendarPopup(True)
        self.form_layout.addRow("Landing Time", self.landing_input)

        # Price input field
        self.price_input = QLineEdit(self)
        self.form_layout.addRow("Price", self.price_input)

        layout.addLayout(self.form_layout)

        # Submit button
        self.submit_button = QPushButton("Add Flight", self)
        self.submit_button.clicked.connect(self.add_flight)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_flight(self):
        """Collect the form data and send to controller for validation and saving."""
        try:
            aircraft_id = self.aircraft_dropdown.currentData()
            source = self.source_input.text()
            destination = self.destination_input.text()
            departure_datetime = self.departure_input.dateTime().toPython()
            landing_datetime = self.landing_input.dateTime().toPython()
            price = float(self.price_input.text())

            # Send the collected data to the controller for validation and saving
            self.controller.save_flight(aircraft_id, source, destination, departure_datetime, landing_datetime, price)

        except ValueError as ve:
            self.controller.show_error_message(f"Invalid input: {ve}")
