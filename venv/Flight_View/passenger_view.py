from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PySide6.QtCore import Qt, QTimer, QCoreApplication

class PassengerView(QWidget):
    def __init__(self, controller=None, user=None):
        super().__init__(parent=None)
        self.controller = controller
        self.user = user  # Store user information

        main_layout = QVBoxLayout()

        # Top layout for "Go Back" button aligned to the left
        top_layout = QHBoxLayout()
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.setStyleSheet("""
            background-color: #3498db; 
            color: white; 
            padding: 10px; 
            font-size: 14px; 
            border-radius: 5px;
        """)
        self.back_button.clicked.connect(self.controller.go_back)
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()  # Pushes the button to the left

        main_layout.addLayout(top_layout)

        # Greeting the user with "Hello {user.firstname}"
        self.greeting_label = QLabel(f"Welcome back!", self)
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setStyleSheet("""
            font-size: 50px; 
            font-weight: bold; 
            color: #2c3e50;
            background-color: #f2f2f2;
            padding: 20px;
        """)
        main_layout.addWidget(self.greeting_label)

        # Buttons section
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(20, 0, 20, 0)

        # Button to view available flights
        self.flights_button = self.create_button("Flights", self.show_loading_and_fetch_flights)
        buttons_layout.addWidget(self.flights_button)

        # Button to view upcoming landings
        self.landings_button = self.create_button("Watch Landings", self.show_loading_and_fetch_landings)
        buttons_layout.addWidget(self.landings_button)

        # Button to view booked flights
        self.my_flights_button = self.create_button("My Flights", self.show_loading_and_fetch_my_flights)
        buttons_layout.addWidget(self.my_flights_button)

        main_layout.addLayout(buttons_layout)
        
        # Adding a spacer to push buttons up
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Loading square
        self.loading_square = self.create_loading_square()
        main_layout.addWidget(self.loading_square)
        self.loading_square.hide()  # Hide the loading square initially

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #f2f2f2;")  # Light gray background
        self.set_background_image('venv/Flight_View/icons/background-sky.jpg')  # Correct path with forward slashes

    def set_background_image(self, image_path):
        """Set the background image of the entire widget."""
        self.setStyleSheet(f"""
            PassengerView {{
                background-image: url({image_path});
                background-position: center;
                background-repeat: no-repeat;
                background-color: rgba(255, 255, 255, 150);  
            }}
        """)

    def create_button(self, text, callback):
        """Helper function to create consistent styled buttons."""
        button = QPushButton(text, self)
        button.setStyleSheet("""
            background-color: #3498db;
            color: white;
            padding: 15px;
            font-size: 16px;
            border-radius: 8px;
        """)
        button.setMinimumHeight(50)  # Make buttons taller
        button.clicked.connect(callback)
        return button

    def create_loading_square(self):
        """Creates a small, sleek loading square with a blue border and centered text."""
        loading_frame = QFrame(self)
        loading_frame.setStyleSheet("""
            background-color: white;
            border: 3px solid #3498db;  /* Blue border */
            border-radius: 10px;
        """)
        loading_frame.setFixedSize(250, 150)  # Define a square-like proportion
        loading_layout = QVBoxLayout()

        # Loading text with centered alignment
        loading_label = QLabel("Just a moment,\n loading all the information...", self)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet("""
            font-size: 16px;
            color: #3498db;  /* Blue text */
            font-weight: bold;
        """)
        loading_layout.addWidget(loading_label)

        loading_frame.setLayout(loading_layout)
        return loading_frame

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

    def show_loading_and_fetch_flights(self):
        """ Show loading and then fetch flights """
        self.show_loading_square()
        QCoreApplication.processEvents()
        QTimer.singleShot(500, self.fetch_flights)

    def show_loading_and_fetch_landings(self):
        """ Show loading and then fetch landings """
        self.show_loading_square()
        QCoreApplication.processEvents()
        QTimer.singleShot(500, self.fetch_landings)

    def show_loading_and_fetch_my_flights(self):
        """ Show loading and then fetch my flights """
        self.show_loading_square()
        QCoreApplication.processEvents()
        QTimer.singleShot(500, self.fetch_my_flights)

    def fetch_flights(self):
        """ Fetch flights and hide loading square """
        self.controller.show_flights()
        self.hide_loading_square()

    def fetch_landings(self):
        """ Fetch landings and hide loading square """
        self.controller.watch_landings()
        self.hide_loading_square()

    def fetch_my_flights(self):
        """ Fetch my flights and hide loading square """
        self.controller.show_my_flights()
        self.hide_loading_square()

    def show_error(self, message):
        """ Display an error message in red """
        self.error_label = QLabel(message, self)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.error_label)
