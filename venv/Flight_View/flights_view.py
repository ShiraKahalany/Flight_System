from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from mock_data import flights, aircrafts

class FlightsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        # Create a table to display flights
        self.table = QTableWidget(self)
        self.table.setRowCount(len(flights))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Flight ID", "Aircraft", "Source", "Destination", "Departure", "Landing"])

        # Populate the table with flight data
        for row, flight in enumerate(flights):
            self.table.setItem(row, 0, QTableWidgetItem(str(flight['id'])))
            aircraft = next((a for a in aircrafts if a['id'] == flight['aircraft_id']), None)
            self.table.setItem(row, 1, QTableWidgetItem(aircraft['nickname']))
            self.table.setItem(row, 2, QTableWidgetItem(flight['source']))
            self.table.setItem(row, 3, QTableWidgetItem(flight['destination']))
            self.table.setItem(row, 4, QTableWidgetItem(flight['departure_datetime'].strftime('%Y-%m-%d %H:%M')))
            self.table.setItem(row, 5, QTableWidgetItem(flight['landing_datetime'].strftime('%Y-%m-%d %H:%M')))

        layout.addWidget(self.table)
        self.setLayout(layout)

    def go_back(self):
        """ Calls go_back from the main application window """
        if self.parent() and hasattr(self.parent(), 'go_back'):
            self.parent().go_back()
