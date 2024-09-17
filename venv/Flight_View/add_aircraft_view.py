from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel

class AddAircraftView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller  # Reference to the AdminController
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        self.back_button.clicked.connect(self.controller.go_back)
        layout.addWidget(self.back_button)

        # Create a form for adding new aircraft
        self.form_layout = QFormLayout()
        self.manufacturer_input = QLineEdit(self)
        self.nickname_input = QLineEdit(self)
        self.year_input = QLineEdit(self)
        self.image_url_input = QLineEdit(self)

        self.form_layout.addRow("Manufacturer", self.manufacturer_input)
        self.form_layout.addRow("Nickname", self.nickname_input)
        self.form_layout.addRow("Year of Manufacture", self.year_input)
        self.form_layout.addRow("Image URL", self.image_url_input)

        layout.addLayout(self.form_layout)

        # Submit button
        self.submit_button = QPushButton("Add Aircraft", self)
        self.submit_button.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        self.submit_button.clicked.connect(self.submit_aircraft)
        layout.addWidget(self.submit_button)

        # Message label for errors or success
        self.message_label = QLabel("")
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def submit_aircraft(self):
        """Handle the submission of the aircraft form."""
        manufacturer = self.manufacturer_input.text().strip()
        nickname = self.nickname_input.text().strip()
        year_of_manufacture = self.year_input.text().strip()
        image_url = self.image_url_input.text().strip()

        if not manufacturer or not nickname or not year_of_manufacture or not image_url:
            self.message_label.setText("All fields are required.")
            self.message_label.setStyleSheet("color: red;")
            return

        # Pass the aircraft data to the controller to save
        self.controller.save_aircraft(manufacturer, nickname, year_of_manufacture, image_url)
