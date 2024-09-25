from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt, QTimer, QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize  


class PassengerView(QWidget):
    def __init__(self, controller=None, user=None):
        super().__init__(parent=None)
        self.controller = controller
        self.user = user

        # Create the main layout with reduced spacing
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)  # Adjust this value to reduce space

        # Top layout for "Go Back" button aligned to the left
        top_layout = QHBoxLayout()

        self.back_button = QPushButton(self)
        self.back_button.setIcon(QIcon(r"Flight_View\icons\back.png"))  # Replace with the actual path to your icon
        self.back_button.setIconSize(QSize(20, 20))  # Adjust icon size as needed

        # Apply styles to make the button circular
        self.back_button.setStyleSheet("""
            background-color: white; 
            border-radius: 18px;  /* Circular button with a radius of 16px */
            border: 2px solid #3498db;  /* Blue border */
            min-width: 36px;  /* Button size equal to twice the radius */
            min-height: 36px; /* Button size equal to twice the radius */
            max-width: 36px;  /* Ensures button is a square */
            max-height: 36px; /* Ensures button is a square */
        """)
        self.back_button.clicked.connect(self.controller.go_back)

        top_layout.addWidget(self.back_button)
        top_layout.addStretch()  # Pushes the button to the left

        main_layout.addLayout(top_layout)

        # Greeting the user with "Welcome back {user.first_name}!"
        self.greeting_label = QLabel(f"Welcome back {self.user.first_name}!", self)
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setStyleSheet("""
            font-size: 50px; 
            font-weight: bold; 
            color: #2c3e50;
            background-color: transparent;  /* Transparent background */
            padding: 10px;  /* Adjust padding to reduce vertical space */
        """)
        main_layout.addWidget(self.greeting_label)

        # Buttons section in a row (HBoxLayout)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(20, 0, 20, 200)

        # Button to view available flights
        self.flights_button = self.create_button("Flights", self.show_loading_and_fetch_flights, icon_path=r"Flight_View\icons\airplane.png")
        buttons_layout.addWidget(self.flights_button)

        # Button to view upcoming landings
        self.landings_button = self.create_button("Watch Landings", self.show_loading_and_fetch_landings, icon_path=r"Flight_View\icons\airplane.png")
        buttons_layout.addWidget(self.landings_button)

        # Button to view booked flights
        self.my_flights_button = self.create_button("My Flights", self.show_loading_and_fetch_my_flights, icon_path=r"Flight_View\icons\airplane.png")
        buttons_layout.addWidget(self.my_flights_button)

        # Add buttons_layout (with buttons in a row) to the main layout
        main_layout.addLayout(buttons_layout)
        
        # Set the layout for the main content
        self.setLayout(main_layout)

        # Create the loading square outside of the layout
        self.loading_square = self.create_loading_square()
        self.loading_square.hide()  # Hide the loading square initially
        

    def create_button(self, text, callback, icon_path=None):
        """Helper function to create consistent styled buttons with optional icons."""
        button = QPushButton(text, self)
        
        # Add icon if icon_path is provided
        if icon_path:
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(40, 40))  # Set the icon size as needed

        # Adjust the style to add space between the icon and text
        button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #3498db;
                padding: 10px;
                font-size: 20px;
                border-radius: 25px;
                border: 2px solid #3498db;  /* Blue border */
                text-align: left;  /* Make text and icon inline */
                padding-left: 20px;  /* Add space between the icon and text */
            }
        """)

        button.setIconSize(QSize(40, 40))  # Adjust icon size
        button.setMinimumHeight(100)  # Make buttons taller to fit both icon and text
        button.setMinimumWidth(150)  # Set minimum width to make them look like squares
        button.clicked.connect(callback)
        return button


    
    def paintEvent(self, event):
        painter = QPainter(self)

        # Correct the path to the image
        pixmap = QPixmap(r"Flight_View/icons/backgroundSky.png")  # Raw string to avoid escape issues

        # Check if the image was loaded correctly
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)
        else:
            print("Image could not be loaded.")

    def create_loading_square(self):
        """Creates a small, sleek loading square with a blue border and centered text."""
        loading_frame = QFrame(self)  # Make it a child of the main widget, not part of the layout
        loading_frame.setStyleSheet("""
            background-color: white;
            border: 3px solid #000000;  /* Blue border */
            border-radius: 10px;
        """)
        loading_frame.setFixedSize(250, 180)  # Define a square-like proportion
        loading_layout = QVBoxLayout()

        # Loading text with centered alignment
        loading_label = QLabel("Just a moment,\n loading all the information...", self)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet("""
            font-size: 16px;
            color: #000000;  /* Blue text */
            font-weight: bold;
        """)
        loading_layout.addWidget(loading_label)

        loading_frame.setLayout(loading_layout)
        return loading_frame

    def show_loading_square(self):
        """ Show the loading square widget in the center of the page """
        self.loading_square.show()
        self.loading_square.raise_()  # Ensure the loading square appears above other widgets

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
