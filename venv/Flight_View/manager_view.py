from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class ManagerView(QWidget):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        # Button to show flights
        self.flights_button = QPushButton("Flights", self)
        self.flights_button.clicked.connect(self.show_flights)
        layout.addWidget(self.flights_button)

        # Button to watch landings
        self.watch_landings_button = QPushButton("Watch Landings", self)
        self.watch_landings_button.clicked.connect(self.watch_landings)
        layout.addWidget(self.watch_landings_button)

        # Button to view booked flights
        self.my_flights_button = QPushButton("My Flights", self)
        self.my_flights_button.clicked.connect(self.show_my_flights)
        layout.addWidget(self.my_flights_button)

        # Admin-specific buttons
        self.add_aircraft_button = QPushButton("Add Aircraft", self)
        self.add_aircraft_button.clicked.connect(self.add_aircraft)
        layout.addWidget(self.add_aircraft_button)

        self.add_flight_button = QPushButton("Add Flight", self)
        self.add_flight_button.clicked.connect(self.add_flight)
        layout.addWidget(self.add_flight_button)

        self.setLayout(layout)

    def go_back(self):
        """ Calls go_back from the main application window """
        if self.parent() and hasattr(self.parent(), 'go_back'):
            self.parent().go_back()

    def show_flights(self):
        from flights_view import FlightsView
        self.parent().set_view(FlightsView(self))

    def watch_landings(self):
        from landings_view import LandingsView
        self.parent().set_view(LandingsView(self))

    def show_my_flights(self):
        from my_flights_view import MyFlightsView
        self.parent().set_view(MyFlightsView(self, self.user))

    def add_aircraft(self):
        from add_aircraft_view import AddAircraftView
        self.parent().set_view(AddAircraftView(self))

    def add_flight(self):
        # Logic to add a flight (future implementation)
        pass
