from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class PassengerView(QWidget):
    def __init__(self, controller=None):
        super().__init__(parent=None)
        self.controller = controller
        self.error_label = QLabel("", self)  # A label to show errors and success messages
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
        self.landings_button.clicked.connect(self.controller.watch_landings)  # Logic in controller
        layout.addWidget(self.landings_button)

        # Button to view booked flights
        self.my_flights_button = QPushButton("My Flights", self)
        self.my_flights_button.clicked.connect(self.controller.show_my_flights)
        layout.addWidget(self.my_flights_button)

        # Add error/success label to the layout
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def show_error(self, message):
        """ Display an error message in the error_label """
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: red;")  # Set the text color to red to indicate an error

    def show_success(self, message):
        """ Display a success message in the error_label """
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: green;")  # Set the text color to green to indicate success
