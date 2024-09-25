from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QTimer, QCoreApplication
from PySide6.QtCore import QSize  

class ManagerView(QWidget):
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

        self.greeting_label = QLabel(f"Hi {self.user.first_name}!", self)
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setStyleSheet("""
            font-size: 60px; 
            font-weight: bold; 
            color: #2c3e50;
            background-color: transparent;  /* Transparent background */
            padding: 10px;  /* Adjust padding to reduce vertical space */
        """)
        main_layout.addWidget(self.greeting_label)

        self.ask_label = QLabel(f"What do you want to do today?", self)
        self.ask_label.setAlignment(Qt.AlignCenter)
        self.ask_label.setStyleSheet("""
            font-size: 30px; 
            color: #2c3e50;
            background-color: transparent;  /* Transparent background */
            padding: 10px;  /* Adjust padding to reduce vertical space */
        """)
        main_layout.addWidget(self.ask_label)

        # Buttons section in a row (HBoxLayout)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(20, 0, 20, 200)

        # Manager-specific buttons with the same style as the passenger buttons
        self.add_aircraft_button = self.create_button("Add Aircraft", self.controller.add_aircraft)
        buttons_layout.addWidget(self.add_aircraft_button)

        self.add_flight_button = self.create_button("Add Flight", self.controller.add_flight)
        buttons_layout.addWidget(self.add_flight_button)

        # Modified buttons with loading square logic
        self.all_flights_button = self.create_button("All Coming Flights", self.show_loading_and_fetch_all_flights)
        buttons_layout.addWidget(self.all_flights_button)

        self.purchase_summary_button = self.create_button("Purchase Summary", self.show_loading_and_fetch_purchase_summary)
        buttons_layout.addWidget(self.purchase_summary_button)

        # Add buttons_layout (with buttons in a row) to the main layout
        main_layout.addLayout(buttons_layout)
        
        # Set the layout for the main content
        self.setLayout(main_layout)

        # Create the loading square outside of the layout
        self.loading_square = self.create_loading_square()
        self.loading_square.hide()  # Hide the loading square initially
        
    def create_button(self, text, callback):
        """Helper function to create consistent styled buttons."""
        button = QPushButton(text, self)
        button.setStyleSheet("""
            background-color: #ffffff;
            color: #3498db;
            padding: 10px;
            font-size: 20px;
            border-radius: 25px;
            border: 2px solid #3498db;  /* Blue border */
        """)
        button.setMinimumHeight(50)  # Make buttons taller
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

    def show_loading_and_fetch_all_flights(self):
        """ Show loading and then fetch all flights """
        self.show_loading_square()
        QCoreApplication.processEvents()
        QTimer.singleShot(500, self.fetch_all_flights)

    def show_loading_and_fetch_purchase_summary(self):
        """ Show loading and then fetch purchase summary """
        self.show_loading_square()
        QCoreApplication.processEvents()
        QTimer.singleShot(500, self.fetch_purchase_summary)

    def fetch_all_flights(self):
        """ Fetch all flights and hide loading square """
        self.controller.show_all_flights()
        self.hide_loading_square()

    def fetch_purchase_summary(self):
        """ Fetch purchase summary and hide loading square """
        self.controller.show_purchase_summary()
        self.hide_loading_square()
