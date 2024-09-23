from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QApplication
from PySide6.QtCore import Qt, QTimer

class PassengerView(QWidget):
    def __init__(self, controller=None):
        super().__init__(parent=None)
        self.controller = controller
        self.error_label = QLabel("", self)  # A label to show errors and success messages
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.go_back_and_hide_loading)  # Hide loading when going back
        layout.addWidget(self.back_button)

        # Button to view available flights
        self.flights_button = QPushButton("Flights", self)
        self.flights_button.clicked.connect(self.show_loading_and_fetch_flights)
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

        # Add loading square (Initially hidden)
        self.loading_square = self.create_loading_square()
        layout.addWidget(self.loading_square)
        self.loading_square.hide()  # Hide the loading square initially

        self.setLayout(layout)

    def create_loading_square(self):
        """Creates a small loading square to show while data is loading."""
        loading_frame = QFrame(self)
        loading_frame.setStyleSheet("background-color: lightgray; border: 2px solid gray;")
        loading_frame.setFixedSize(200, 100)  # Small square
        loading_layout = QVBoxLayout()

        loading_label = QLabel("Please wait...\nLoading flights...", self)
        loading_label.setAlignment(Qt.AlignCenter)  # Center the text within the label
        loading_layout.addWidget(loading_label)
        loading_frame.setLayout(loading_layout)

        return loading_frame

    def show_loading_and_fetch_flights(self):
        """ Show the loading square, force UI refresh, and fetch flights """
        self.show_loading_square()  # Show the loading square

        # Force UI refresh
        QApplication.processEvents()

        # Simulate delay before showing flights (optional)
        QTimer.singleShot(500, self.fetch_flights)

    def fetch_flights(self):
        """ Fetch flights and hide loading after switching view """
        self.controller.show_flights()  # Call the controller to fetch flights
        self.hide_loading_square()  # Ensure the loading square is hidden when flights are shown

    def show_loading_square(self):
        """ Show the loading square widget in the center of the page """
        self.loading_square.show()

        # Dynamically center the loading square
        window_width = self.width()
        window_height = self.height()
        square_width = self.loading_square.width()
        square_height = self.loading_square.height()

        self.loading_square.move(
            (window_width - square_width) // 2,
            (window_height - square_height) // 2
        )

    def hide_loading_square(self):
        """ Hide the loading square widget """
        self.loading_square.hide()

    def go_back_and_hide_loading(self):
        """ Go back and hide the loading square """
        self.hide_loading_square()  # Ensure loading square is hidden when going back
        self.controller.go_back()

    def show_error(self, message):
        """ Display an error message in the error_label """
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: red;")  # Set the text color to red to indicate an error

    def show_success(self, message):
        """ Display a success message in the error_label """
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: green;")  # Set the text color to green to indicate success
