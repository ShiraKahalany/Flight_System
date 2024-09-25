from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ManagerFlightsView(QWidget):
    def __init__(self, controller=None, flights=None):
        super().__init__()
        self.controller = controller
        self.flights = flights
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.setStyleSheet("""
            background-color: #3498db; 
            color: white; 
            padding: 10px; 
            font-size: 14px; 
            border-radius: 5px;
        """)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        # Create a table to display flights
        self.table = QTableWidget(self)
        self.table.setRowCount(len(self.flights))
        self.table.setColumnCount(8)  # 8 columns, without the Action column
        self.table.setHorizontalHeaderLabels(["Aircraft Image", "ID", "Aircraft", "Source", "Destination", "Departure", "Landing", "Price"])

        # Set column width to make it wider
        self.table.setColumnWidth(0, 100)  # Aircraft Image
        self.table.setColumnWidth(1, 40)   # Flight ID
        self.table.setColumnWidth(2, 100)  # Aircraft
        self.table.setColumnWidth(3, 100)  # Source
        self.table.setColumnWidth(4, 120)  # Destination
        self.table.setColumnWidth(5, 120)  # Departure
        self.table.setColumnWidth(6, 120)  # Landing
        self.table.setColumnWidth(7, 80)   # Price

        # Populate the table with flight data
        for row, flight in enumerate(self.flights):
            if flight.aircraft:
                # Add image to the first column
                image_label = QLabel()
                if flight.aircraft.image_data:
                    pixmap = QPixmap()
                    pixmap.loadFromData(flight.aircraft.image_data)
                    pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio)  # Scale the image
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("No Image")

                self.table.setCellWidget(row, 0, image_label)

            self.table.setItem(row, 1, QTableWidgetItem(str(flight.id)))
            self.table.setItem(row, 2, QTableWidgetItem(flight.aircraft.nickname if flight.aircraft else "Unknown"))
            self.table.setItem(row, 3, QTableWidgetItem(flight.source))
            self.table.setItem(row, 4, QTableWidgetItem(flight.destination))
            self.table.setItem(row, 5, QTableWidgetItem(flight.departure_datetime.strftime('%Y-%m-%d %H:%M')))
            self.table.setItem(row, 6, QTableWidgetItem(flight.landing_datetime.strftime('%Y-%m-%d %H:%M')))
            self.table.setItem(row, 7, QTableWidgetItem(f"${flight.price}"))  # Display the price

        layout.addWidget(self.table)
        self.setLayout(layout)

    def go_back(self):
        """ Calls go_back from the main application window """
        if self.parent() and hasattr(self.parent(), 'go_back'):
            self.parent().go_back()
