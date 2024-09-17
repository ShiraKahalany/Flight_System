import requests  # For downloading images from the internet
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from Flight_View.mock_data import flights, aircrafts

class FlightsView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        # Create a table to display flights
        self.table = QTableWidget(self)
        self.table.setRowCount(len(flights))
        self.table.setColumnCount(8)  # Add one more column for the Aircraft Image
        self.table.setHorizontalHeaderLabels(["Aircraft Image", "ID", "Aircraft", "Source", "Destination", "Departure", "Landing", "Action"])

        # Set column width to make it wider
        self.table.setColumnWidth(0, 100)  # Aircraft Image
        self.table.setColumnWidth(1, 40)   # Flight ID
        self.table.setColumnWidth(2, 100)  # Aircraft
        self.table.setColumnWidth(3, 100)  # Source
        self.table.setColumnWidth(4, 120)  # Destination
        self.table.setColumnWidth(5, 120)  # Departure
        self.table.setColumnWidth(6, 120)  # Landing
        self.table.setColumnWidth(7, 60)   # Action

        # Populate the table with flight data and add "Watch" buttons
        for row, flight in enumerate(flights):
            aircraft = self.controller.get_aircraft_by_id(flight.aircraft_id)
            if aircraft:
                # Add image to the first column
                image_label = QLabel()

                # Download image from URL
                image_data = self.download_image(aircraft.image_url)
                if image_data:
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio)  # Scale the image
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("No Image")

                self.table.setCellWidget(row, 0, image_label)

            self.table.setItem(row, 1, QTableWidgetItem(str(flight.id)))
            self.table.setItem(row, 2, QTableWidgetItem(aircraft.nickname if aircraft else "Unknown"))
            self.table.setItem(row, 3, QTableWidgetItem(flight.source))
            self.table.setItem(row, 4, QTableWidgetItem(flight.destination))
            self.table.setItem(row, 5, QTableWidgetItem(flight.departure_datetime.strftime('%Y-%m-%d %H:%M')))
            self.table.setItem(row, 6, QTableWidgetItem(flight.landing_datetime.strftime('%Y-%m-%d %H:%M')))

            # Add the "Watch" button
            watch_button = QPushButton("Watch", self)
            watch_button.clicked.connect(lambda _, f=flight: self.watch_flight(f))
            self.table.setCellWidget(row, 7, watch_button)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def download_image(self, url):
        """Download the image from the given URL and return its binary content."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses
            return response.content  # Return image data as bytes
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None

    def watch_flight(self, flight):
        """ Call the controller to show flight details """
        self.controller.show_flight_details(flight.id)

    def go_back(self):
        """ Calls go_back from the main application window """
        if self.parent() and hasattr(self.parent(), 'go_back'):
            self.parent().go_back()
