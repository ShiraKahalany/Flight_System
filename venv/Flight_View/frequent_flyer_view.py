from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class FrequentFlyerView(QWidget):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.parent().go_back)
        layout.addWidget(self.back_button)

        self.flights_button = QPushButton("Flights", self)
        self.flights_button.clicked.connect(self.show_flights)
        layout.addWidget(self.flights_button)

        self.watch_landings_button = QPushButton("Watch Landings", self)
        self.watch_landings_button.clicked.connect(self.watch_landings)
        layout.addWidget(self.watch_landings_button)

        self.my_flights_button = QPushButton("My Flights", self)
        self.my_flights_button.clicked.connect(self.show_my_flights)
        layout.addWidget(self.my_flights_button)

        self.setLayout(layout)

    def show_flights(self):
        from flights_view import FlightsView
        self.parent().set_view(FlightsView(self))

    def watch_landings(self):
        from landings_view import LandingsView
        self.parent().set_view(LandingsView(self))

    def show_my_flights(self):
        from my_flights_view import MyFlightsView
        self.parent().set_view(MyFlightsView(self, self.user))
