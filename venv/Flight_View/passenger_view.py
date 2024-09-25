from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt, QTimer, QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class PassengerView(QWidget):
    def __init__(self, controller=None, user=None, date_details=None):
        super().__init__(parent=None)
        self.controller = controller
        self.user = user
        self.date_details = date_details

        # Create the main layout with reduced spacing
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)  # Adjust this value to reduce space

        # Top layout for "Go Back" button and date details in the same row
        top_layout = QHBoxLayout()

        # "Go Back" button
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

        # Add stretch to push the date details to the right
        top_layout.addStretch()

        # Add date details at the top in a row with a semi-transparent white background
        date_frame = QFrame(self)
        date_frame.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.05);  /* Semi-transparent white */
            border-radius: 15px;  /* Rounded corners */
            padding: 5px;  /* Reduced padding */
        """)

        # Set a fixed height for the frame to remove excess space
        date_frame.setFixedHeight(50)  # Adjust the height to fit the content

        date_layout = QHBoxLayout()
        date_layout.setContentsMargins(5, 5, 5, 5)  # Remove extra margins
        date_layout.setSpacing(15)  # Adjust spacing between date labels

        shabbat_start = self.date_details.shabbat_start.strftime("%H:%M")
        shabbat_end = self.date_details.shabbat_end.strftime("%H:%M")
        parasha = self.date_details.parasha
        hebrew_date = self.date_details.hebrew_date
        days_of_week = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
        day = days_of_week[self.date_details.day_of_week]
        
        # Create QLabel for each date detail with style
        shabbat_start_label = QLabel(f"Shabbat Start: {shabbat_start}", self)
        shabbat_end_label = QLabel(f"Shabbat End: {shabbat_end}", self)
        parasha_label = QLabel(f"{parasha}", self)
        hebrew_date_label = QLabel(f"{hebrew_date}", self)
        day_label = QLabel(f"{day}", self)

        # Apply consistent styling for readability
        label_style = """
            font-size: 16px; 
            color: #2c3e50;
            font-weight: bold;
            background-color: transparent;
        """
        
        shabbat_start_label.setStyleSheet(label_style)
        shabbat_end_label.setStyleSheet(label_style)
        parasha_label.setStyleSheet(label_style)
        hebrew_date_label.setStyleSheet(label_style)
        day_label.setStyleSheet(label_style)

        # Add labels to the layout (in a row)
        date_layout.addWidget(shabbat_start_label)
        date_layout.addSpacing(20)
        date_layout.addWidget(shabbat_end_label)
        date_layout.addSpacing(20)
        date_layout.addWidget(parasha_label)
        date_layout.addSpacing(20)
        date_layout.addWidget(hebrew_date_label)
        date_layout.addSpacing(20)
        date_layout.addWidget(day_label)

        # Set the date_layout into the date_frame
        date_frame.setLayout(date_layout)

        # Add the date_frame to the top layout (pushed to the right)
        top_layout.addWidget(date_frame)

        # Add top layout (containing the back button and date details) to the main layout
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
        self.flights_button = self.create_button("  All Flights", self.show_loading_and_fetch_flights, icon_path=r"Flight_View\icons\worldPlane.png")
        buttons_layout.addWidget(self.flights_button)

        # Button to view upcoming landings
        self.landings_button = self.create_button("  Watch Landings", self.show_loading_and_fetch_landings, icon_path=r"Flight_View\icons\landings.png")
        buttons_layout.addWidget(self.landings_button)

        # Button to view booked flights
        self.my_flights_button = self.create_button("   My Flights", self.show_loading_and_fetch_my_flights, icon_path=r"Flight_View\icons\ticket.png")
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
            button.setIconSize(QSize(40,40))  # Set the icon size as needed

        # Adjust the style to add space between the icon and text
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.6);
                color: #2c3e50;
                padding: 10px;
                font-weight: bold;
                font-size: 25px;
                border-radius: 25px;
                border: 2px solid #3498db;  /* Blue border */
                text-align: center;  /* Make text and icon inline */
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
            background-color: rgba(0,0,0,0.65);
            border: 1px  #34cfff;  /* Blue border */
            border-radius: 20px;
        """)
        loading_frame.setFixedSize(240, 110)  # Define a square-like proportion
        loading_layout = QVBoxLayout()

        # Loading text with centered alignment
        loading_label = QLabel("Just a moment,\n loading all the information...", self)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet("""
            font-size: 16px;
            background-color: transparent;  /* Transparent background */
            color: #34cfff;  /* Blue text */
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
