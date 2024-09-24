import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class LandingsView(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller  # Pass the controller to access logic
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.controller.go_back)  # Use controller logic for going back
        layout.addWidget(self.back_button)

        # Dropdown to select hours ahead (1 to 5) with 1 hour selected by default
        self.time_dropdown = QComboBox(self)
        self.time_dropdown.addItems(['1 hour', '2 hours', '3 hours', '4 hours', '5 hours'])
        self.time_dropdown.setCurrentIndex(0)  # Set default to 1 hour
        self.time_dropdown.currentIndexChanged.connect(self.update_landings)
        layout.addWidget(self.time_dropdown)

        # Create a table to display landings with images and predictions
        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(7)  # Add a column for the Landing Prediction
        self.table.setHorizontalHeaderLabels(["Image", "Flight ID", "Source", "Destination", "Departure", "Landing", "Prediction"])
        layout.addWidget(self.table)

        # Set initial column widths
        self.table.setColumnWidth(0, 80)  # Image
        self.table.setColumnWidth(1, 60)  # Flight ID
        self.table.setColumnWidth(2, 100)  # Source
        self.table.setColumnWidth(3, 120)  # Destination
        self.table.setColumnWidth(4, 120)  # Departure
        self.table.setColumnWidth(5, 120)  # Landing
        self.table.setColumnWidth(6, 100)  # Prediction

        self.setLayout(layout)

        # Call the update_landings function when the view is first shown
        self.update_landings()

    def update_landings(self):
        """Update the landing flights table based on the hours ahead selected."""
        hours_ahead = int(self.time_dropdown.currentText().split()[0])

        # Use controller to get the upcoming landings based on the selected hours
        filtered_flights = self.controller.get_upcoming_landings(hours_ahead)

        self.table.setRowCount(len(filtered_flights))

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

    def go_back(self):
        """ Calls go_back from the controller """
        if self.controller:
            self.controller.go_back()
