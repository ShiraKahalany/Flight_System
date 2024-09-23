from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

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
        self.flights_button = self.create_button("Flights", self.controller.show_flights)
        buttons_layout.addWidget(self.flights_button)

        # Button to view upcoming landings
        self.landings_button = self.create_button("Watch Landings", self.controller.watch_landings)
        buttons_layout.addWidget(self.landings_button)

        # Button to view booked flights
        self.my_flights_button = self.create_button("My Flights", self.controller.show_my_flights)
        buttons_layout.addWidget(self.my_flights_button)

        main_layout.addLayout(buttons_layout)
        
        # Adding a spacer to push buttons up
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #f2f2f2;")  # Light gray background

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

    def show_error(self, message):
        """ Display an error message in red """
        self.error_label = QLabel(message, self)
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.error_label)

