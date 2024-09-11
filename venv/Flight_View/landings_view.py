from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QPushButton
from datetime import datetime, timedelta
from mock_data import flights

class LandingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        # Dropdown to select hours ahead (1 to 5)
        self.time_dropdown = QComboBox(self)
        self.time_dropdown.addItems(['1 hour', '2 hours', '3 hours', '4 hours', '5 hours'])
        self.time_dropdown.currentIndexChanged.connect(self.update_landings)
        layout.addWidget(self.time_dropdown)

        # Create a table to display landings
        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Flight ID", "Source", "Destination", "Departure", "Landing"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def update_landings(self):
        hours_ahead = int(self.time_dropdown.currentText().split()[0])
        now = datetime.now()
        future_time = now + timedelta(hours=hours_ahead)

        # Filter flights landing at Ben Gurion Airport within the time window
        filtered_flights = [f for f in flights if f['destination'] == "Ben Gurion Airport" and now <= f['landing_datetime'] <= future_time]

        self.table.setRowCount(len(filtered_flights))

        # Populate the table with filtered flight data
        for row, flight in enumerate(filtered_flights):
            self.table.setItem(row, 0, QTableWidgetItem(str(flight['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(flight['source']))
            self.table.setItem(row, 2, QTableWidgetItem(flight['destination']))
            self.table.setItem(row, 3, QTableWidgetItem(flight['departure_datetime'].strftime('%Y-%m-%d %H:%M')))
            self.table.setItem(row, 4, QTableWidgetItem(flight['landing_datetime'].strftime('%Y-%m-%d %H:%M')))

    def go_back(self):
        """ Calls go_back from the main application window """
        if self.parent() and hasattr(self.parent(), 'go_back'):
            self.parent().go_back()
