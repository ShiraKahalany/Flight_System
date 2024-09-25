import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QFrame, QHeaderView
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtCore import Qt, QSize

class LandingsView(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller  # Pass the controller to access logic

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)  # Adjust to make it more compact

        # "Go Back" Button
        self.back_button = QPushButton(self)
        self.back_button.setIcon(QIcon(r"Flight_View/icons/back.png"))  # Replace with actual path to your icon
        self.back_button.setIconSize(QSize(20, 20))  # Adjust icon size as needed

        # Apply styles to make the button circular
        self.back_button.setStyleSheet("""
            background-color: white; 
            border-radius: 18px;  /* Circular button */
            border: 2px solid #3498db;  /* Blue border */
            min-width: 36px;
            min-height: 36px;
            max-width: 36px;
            max-height: 36px;
        """)
        self.back_button.clicked.connect(self.controller.go_back)
        main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Container for combo box and table (semi-transparent white)
        container = QFrame(self)
        container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.8);  /* Semi-transparent white */
            border-radius: 20px;
            padding: 20px;
        """)
        container.setFixedWidth(800)  # Adjust to make it smaller than the full page width
        container_layout = QVBoxLayout()

        # Dropdown to select hours ahead (1 to 5) with 1 hour selected by default
        self.time_dropdown = QComboBox(self)
        self.time_dropdown.addItems(['1 hour', '2 hours', '3 hours', '4 hours', '5 hours'])
        self.time_dropdown.setCurrentIndex(0)  # Set default to 1 hour
        self.time_dropdown.setStyleSheet("""
            QComboBox {
                padding: 10px;
                font-size: 16px;
                background-color: white;
                border: 2px solid #3498db;  /* Blue border */
                border-radius: 10px;
            }
        """)
        self.time_dropdown.currentIndexChanged.connect(self.update_landings)
        container_layout.addWidget(self.time_dropdown)

        # Label to show "No Landings" message
        self.no_landings_label = QLabel(self)
        self.no_landings_label.setStyleSheet("""
            color: #e74c3c;
            font-size: 18px;
            font-weight: bold;
        """)
        self.no_landings_label.setAlignment(Qt.AlignCenter)
        self.no_landings_label.hide()  # Hidden initially

        # Create a table to display landings with images and predictions
        self.table = QTableWidget(self) 
        self.table.setRowCount(0)
        self.table.setColumnCount(7)  # Add a column for the Landing Prediction
        self.table.setHorizontalHeaderLabels(["Image", "Flight ID", "Source", "Destination", "Departure", "Landing", "Prediction"])

        # Set column widths and make headers visible
        self.table.setColumnWidth(0, 80)  # Image
        self.table.setColumnWidth(1, 60)  # Flight ID
        self.table.setColumnWidth(2, 100)  # Source
        self.table.setColumnWidth(3, 120)  # Destination
        self.table.setColumnWidth(4, 120)  # Departure
        self.table.setColumnWidth(5, 120)  # Landing
        self.table.setColumnWidth(6, 100)  # Prediction

        # Make the header visible and adjust its style
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setStyleSheet("font-weight: bold;")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)  # Hide the vertical header

        # Ensure padding/margins do not cut off headers
        self.table.setContentsMargins(0, 10, 0, 10)
        self.table.setStyleSheet("QTableWidget { padding-top: 20px; }")

        # Add table and message label to the container layout
        container_layout.addWidget(self.no_landings_label)  # Will be shown only when no flights
        container_layout.addWidget(self.table)  # Will be collapsed when no flights

        # Set the container layout and add to the main layout
        container.setLayout(container_layout)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

        # Call the update_landings function when the view is first shown
        self.update_landings()

    def update_landings(self):
        """Update the landing flights table based on the hours ahead selected."""
        hours_ahead = int(self.time_dropdown.currentText().split()[0])

        # Use controller to get the upcoming landings based on the selected hours
        filtered_flights = self.controller.get_upcoming_landings(hours_ahead)

        # Clear the table and hide the "no landings" label initially
        self.table.setRowCount(0)
        self.no_landings_label.hide()

        # If there are no flights, show the message and hide the table
        if not filtered_flights:
            self.table.hide()  # Hide the table
            self.no_landings_label.setText(f"No landings in the next {hours_ahead} hours.")
            self.no_landings_label.show()  # Show the no landings message
            return

        # Otherwise, populate the table with the flight data and show it
        self.table.setRowCount(len(filtered_flights))
        self.table.show()  # Ensure the table is visible
        self.no_landings_label.hide()  # Hide the message

        # Populate the table with filtered flight data and images
        for row, flight in enumerate(filtered_flights):
            # Fetch aircraft data from the DAL through the controller
            aircraft = self.controller.dal.Aircraft.get_aircraft_by_id(flight.aircraft_id)
            if aircraft:
                # Add image to the first column
                image_label = QLabel()

                # Download image from URL
                image_data = self.download_image(aircraft.image_url)
                if image_data:
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)  # Scale the image
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("No Image")

                self.table.setCellWidget(row, 0, image_label)

            self.table.setItem(row, 1, QTableWidgetItem(str(flight.id)))
            self.table.setItem(row, 2, QTableWidgetItem(flight.source))
            self.table.setItem(row, 3, QTableWidgetItem(flight.destination))
            self.table.setItem(row, 4, QTableWidgetItem(flight.departure_datetime.strftime('%Y-%m-%d %H:%M')))
            self.table.setItem(row, 5, QTableWidgetItem(flight.landing_datetime.strftime('%Y-%m-%d %H:%M')))

            # Get prediction for landing delay
            is_landing_delayed = self.controller.predict_landing_delay(flight)
            prediction_text = "Delayed" if is_landing_delayed else "On Time"
            self.table.setItem(row, 6, QTableWidgetItem(prediction_text))

    def download_image(self, url):
        """Download the image from the given URL and return its binary content."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses
            return response.content  # Return image data as bytes
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None

    def paintEvent(self, event):
        """ Custom paint event to add the background image. """
        painter = QPainter(self)

        # Load the background image (sky background)
        pixmap = QPixmap(r"Flight_View/icons/backgroundSky.png")  # Replace with the correct path

        # Draw the background image
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)
        else:
            print("Image could not be loaded.")
