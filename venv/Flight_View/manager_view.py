from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class ManagerView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.controller.go_back)  # Logic in controller
        layout.addWidget(self.back_button)

        # Admin-specific buttons
        self.add_aircraft_button = QPushButton("Add Aircraft", self)
        self.add_aircraft_button.clicked.connect(self.controller.add_aircraft)  # Logic in controller
        layout.addWidget(self.add_aircraft_button)

        self.add_flight_button = QPushButton("Add Flight", self)
        self.add_flight_button.clicked.connect(self.controller.add_flight)  # Logic in controller
        layout.addWidget(self.add_flight_button)

        self.setLayout(layout)
