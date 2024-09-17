from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QPushButton

class FlightEntryView(QWidget):
    def __init__(self, controller=None, flight=None):
        super().__init__(parent=None)  # Initialize QWidget with no parent (or specify a QWidget as parent if needed)
        self.controller = controller
        self.flight = flight
        layout = QFormLayout()

        # Display flight details
        layout.addRow("Flight ID:", QLabel(str(self.flight.id)))
        layout.addRow("Aircraft ID:", QLabel(str(self.flight.aircraft_id)))
        layout.addRow("Source:", QLabel(self.flight.source))
        layout.addRow("Destination:", QLabel(self.flight.destination))
        layout.addRow("Departure:", QLabel(self.flight.departure_datetime.strftime('%Y-%m-%d %H:%M')))
        layout.addRow("Landing:", QLabel(self.flight.landing_datetime.strftime('%Y-%m-%d %H:%M')))

        # "Purchase" Button
        self.purchase_button = QPushButton("Purchase", self)
        self.purchase_button.clicked.connect(self.purchase_flight)
        layout.addWidget(self.purchase_button)

        self.setLayout(layout)

    def purchase_flight(self):
        """ Calls the controller to purchase the flight """
        self.controller.purchase_ticket(self.flight.id)
