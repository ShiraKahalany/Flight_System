from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class PassengerView(QWidget):
    def __init__(self, controller=None):
        super().__init__(parent=None)
        self.controller = controller
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.controller.go_back)  # Logic in controller
        layout.addWidget(self.back_button)

        # Button to view available flights
        self.flights_button = QPushButton("Flights", self)
        self.flights_button.clicked.connect(self.controller.show_flights)
        layout.addWidget(self.flights_button)

        # Button to view upcoming landings
        self.landings_button = QPushButton("Watch Landings", self)
        # Fix: Correct method name to `watch_landings`
        self.landings_button.clicked.connect(self.controller.watch_landings)
        layout.addWidget(self.landings_button)

        # Button to view booked flights
        self.my_flights_button = QPushButton("My Flights", self)
        self.my_flights_button.clicked.connect(self.controller.show_my_flights)
        layout.addWidget(self.my_flights_button)

        self.setLayout(layout)
