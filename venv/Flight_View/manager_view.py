from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class ManagerView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
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
        self.back_button.clicked.connect(self.controller.go_back)  # Logic in controller
        layout.addWidget(self.back_button)

        # Admin-specific buttons
        self.add_aircraft_button = QPushButton("Add Aircraft", self)
        self.add_aircraft_button.clicked.connect(self.controller.add_aircraft)  # Logic in controller
        layout.addWidget(self.add_aircraft_button)

        self.add_flight_button = QPushButton("Add Flight", self)
        self.add_flight_button.clicked.connect(self.controller.add_flight)  # Logic in controller
        layout.addWidget(self.add_flight_button)

        # New button for "All Coming Flights"
        self.all_flights_button = QPushButton("All Coming Flights", self)
        self.all_flights_button.clicked.connect(self.controller.show_all_flights)  # Logic in controller
        layout.addWidget(self.all_flights_button)

        # New button for "Purchase Summary"
        self.purchase_summary_button = QPushButton("Purchase Summary", self)
        self.purchase_summary_button.clicked.connect(self.controller.show_purchase_summary)  # Logic in controller
        layout.addWidget(self.purchase_summary_button)

        self.setLayout(layout)
