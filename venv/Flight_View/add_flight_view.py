from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QDateTimeEdit, QLabel, QFrame
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from datetime import datetime

class AddFlightView(QWidget):
    def __init__(self, controller, aircrafts):
        super().__init__()
        self.controller = controller
        self.aircrafts = aircrafts

        # Predefined locations for the dropdowns
        locations = [
            "Tel Aviv", "New York", "London", "Tokyo", "Paris", "Los Angeles", "Dubai", "Singapore", "Hong Kong", "Sydney", 
            "Toronto", "Berlin", "Amsterdam", "Bangkok", "Istanbul", "Moscow", "Mumbai", "São Paulo", "Mexico City", 
            "Johannesburg", "Cairo", "Delhi", "Rome", "Madrid", "Frankfurt", "Seoul", "Chicago", "Kuala Lumpur", 
            "Beijing", "Zurich", "Vienna", "Barcelona", "Miami", "San Francisco", "Vancouver", "Munich", "Copenhagen", 
            "Lisbon", "Stockholm", "Athens", "Dublin", "Prague", "Helsinki", "Abu Dhabi", "Doha", "Riyadh", "Warsaw", 
            "Budapest", "Brussels"
        ]

        # Main layout for the page
        main_layout = QVBoxLayout()

        # "Go Back" Button
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
        main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Create a frame to act as a semi-transparent rectangle container
        container = QFrame(self)
        container_layout = QVBoxLayout()

        # Set the container's style (white background, rounded corners)
        container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.9);  /* Semi-transparent white */
            border-radius: 20px;  /* Rounded corners */
            padding: 20px;
        """)
        container.setFixedWidth(500)  # Set the width of the container to 500px (Adjust as needed)

        # Create a form for adding new flights
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(0)  # Remove vertical spacing between rows

        # Transparent labels
        label_style = "background-color: rgba(255, 255, 255, 0); color: #2c3e50; font-size: 16px;"

        # Aircraft dropdown
        aircraft_label = QLabel("Aircraft", self)
        aircraft_label.setStyleSheet(label_style)
        self.aircraft_dropdown = QComboBox(self)
        for aircraft in self.aircrafts:
            self.aircraft_dropdown.addItem(f"{aircraft.nickname} ({aircraft.manufacturer})", aircraft.id)

        # Style the ComboBox to look cleaner
        self.aircraft_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border-left: 1px solid #3498db;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                border: 1px solid #3498db;
                selection-background-color: #3498db;
            }
        """)
        self.form_layout.addRow(aircraft_label, self.aircraft_dropdown)

        # Source location dropdown
        source_label = QLabel("Source", self)
        source_label.setStyleSheet(label_style)
        self.source_dropdown = QComboBox(self)
        self.source_dropdown.addItems(locations)

        # Style the ComboBox for source
        self.source_dropdown.setStyleSheet(self.aircraft_dropdown.styleSheet())
        self.form_layout.addRow(source_label, self.source_dropdown)

        # Destination location dropdown
        destination_label = QLabel("Destination", self)
        destination_label.setStyleSheet(label_style)
        self.destination_dropdown = QComboBox(self)
        self.destination_dropdown.addItems(locations)

        # Style the ComboBox for destination
        self.destination_dropdown.setStyleSheet(self.aircraft_dropdown.styleSheet())
        self.form_layout.addRow(destination_label, self.destination_dropdown)

        # DateTime inputs for departure and landing
        departure_label = QLabel("Departure Time", self)
        departure_label.setStyleSheet(label_style)
        self.departure_input = QDateTimeEdit(self)
        self.departure_input.setDateTime(datetime.now())
        self.departure_input.setCalendarPopup(True)

        # Style the DateTimeEdit to look better and larger
        self.departure_input.setStyleSheet("""
            QDateTimeEdit {
                background-color: #ffffff;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                min-height: 30px;
            }
        """)
        self.departure_input.setMinimumSize(200, 30)
        self.form_layout.addRow(departure_label, self.departure_input)

        landing_label = QLabel("Landing Time", self)
        landing_label.setStyleSheet(label_style)
        self.landing_input = QDateTimeEdit(self)
        self.landing_input.setDateTime(datetime.now())
        self.landing_input.setCalendarPopup(True)

        # Style the DateTimeEdit for landing input
        self.landing_input.setStyleSheet(self.departure_input.styleSheet())
        self.landing_input.setMinimumSize(200, 30)
        self.form_layout.addRow(landing_label, self.landing_input)

        # Price input field
        price_label = QLabel("Price", self)
        price_label.setStyleSheet(label_style)
        self.price_input = QLineEdit(self)

        # Style the Price input to match the ComboBox
        self.price_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                min-height: 30px;
            }
        """)
        self.price_input.setMinimumSize(200, 30)
        self.form_layout.addRow(price_label, self.price_input)

        # Add the form layout to the container
        container_layout.addLayout(self.form_layout)

        container_layout.setSpacing(20)  # Remove the spacing between the form and other elements

        # Submit button
        self.submit_button = QPushButton("Add Flight", self)
        self.submit_button.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; border-radius: 10px;")
        self.submit_button.clicked.connect(self.add_flight)
        container_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        # Message label for errors or success
        self.message_label = QLabel("")
        self.message_label.setStyleSheet(label_style)
        self.message_label.hide()  # Initially hide the label
        container_layout.addWidget(self.message_label, alignment=Qt.AlignCenter)

        # Set the layout for the container and add it to the main layout
        container.setLayout(container_layout)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)

        # Set the main layout
        self.setLayout(main_layout)

    def paintEvent(self, event):
        """ Custom paint event to add the background image with a dark overlay. """
        painter = QPainter(self)

        # Load the background image
        pixmap = QPixmap(r"Flight_View/icons/backgroundSky.png")  # Replace with the correct path

        # Draw the background image
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)

        # Add a semi-transparent dark overlay to darken the background
        painter.setBrush(Qt.black)
        painter.setOpacity(0.2)  # Adjust opacity to make it darker
        painter.drawRect(self.rect())

    def add_flight(self):
        """Collect the form data and send it to the controller for validation and saving."""
        aircraft_id = self.aircraft_dropdown.currentData()
        source = self.source_dropdown.currentText()
        destination = self.destination_dropdown.currentText()
        departure_datetime = self.departure_input.dateTime().toPython()
        landing_datetime = self.landing_input.dateTime().toPython()
        price = self.price_input.text()

        if not aircraft_id or not source or not destination or not price:
            self.message_label.setText("All fields are required.")
            self.message_label.setStyleSheet("color: red;")
            self.message_label.show()
            return

        # Send the collected data to the controller for validation and saving
        self.controller.save_flight(aircraft_id, source, destination, departure_datetime, landing_datetime, price)

    def show_message(self, message, color="red"):
        """Displays success or error messages to the user."""
        if message:
            self.message_label.setText(message)
            self.message_label.setStyleSheet(f"color: {color};")
            self.message_label.show()  # Show the label when there is a message
        else:
            self.message_label.hide()  # Hide the label if no message
        
        # Trigger a layout update to resize the container
        self.adjustSize()
