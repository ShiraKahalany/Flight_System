from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from mock_data import tickets, flights

class MyFlightsView(QWidget):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.parent().go_back)
        layout.addWidget(self.back_button)

        # Create a table to display booked flights
        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Flight ID", "Source", "Destination", "Departure", "Landing"])

        # Filter tickets by the current user's ID
        user_tickets = [t for t in tickets if t['user_id'] == self.user['id']]

        # Populate the table with flight data from the user's tickets
        self.table.setRowCount(len(user_tickets))

        for row, ticket in enumerate(user_tickets):
            flight = next((f for f in flights if f['id'] == ticket['flight_id']), None)
            if flight:
                self.table.setItem(row, 0, QTableWidgetItem(str(flight['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(flight['source']))
                self.table.setItem(row, 2, QTableWidgetItem(flight['destination']))
                self.table.setItem(row, 3, QTableWidgetItem(flight['departure_datetime'].strftime('%Y-%m-%d %H:%M')))
                self.table.setItem(row, 4, QTableWidgetItem(flight['landing_datetime'].strftime('%Y-%m-%d %H:%M')))

        layout.addWidget(self.table)
        self.setLayout(layout)
