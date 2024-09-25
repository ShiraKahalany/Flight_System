from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QFrame
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize  

class AddAircraftView(QWidget):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller  # Reference to the AdminController

        # Main layout for the page
        main_layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton(self)
        self.back_button.setIcon(QIcon(r"Flight_View\icons\back.png"))  # Replace with the actual path to your icon
        self.back_button.setIconSize(QSize(20, 20))  # Adjust icon size as needed

        # Apply styles to make the button circular
        self.back_button.setStyleSheet("""
            background-color: white; 
            border-radius: 18px;  /* Circular button with a radius of 16px */
            border: 2px solid #3498db;  /* Blue border */
            min-width: 36px;  /* Button size equal to twice the radius */
            min-height: 36px; /* Button size equal to twice the radius */
            max-width: 36px;  /* Ensures button is a square */
            max-height: 36px; /* Ensures button is a square */
        """)
        self.back_button.clicked.connect(self.controller.go_back)
        main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Create a frame to act as a semi-transparent rectangle container
        container = QFrame(self)
        container_layout = QVBoxLayout()

        # Set the container's style (white background, rounded corners)
        container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.9);  /* Semi-transparent white */
            border-radius: 20px;  /* Rounded corners */
            padding: 20px;
        """)
        container.setFixedWidth(500)  # Set the width of the container to 500px (Adjust as needed)

        # Create a form for adding new aircraft
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(0)  # Remove vertical spacing between rows

        # Transparent labels
        label_style = "background-color: rgba(255, 255, 255, 0); color: #2c3e50; font-size: 16px;"

        self.manufacturer_input = QLineEdit(self)
        self.nickname_input = QLineEdit(self)
        self.year_input = QLineEdit(self)
        self.image_url_input = QLineEdit(self)
        self.number_of_chairs_input = QLineEdit(self)

        # Add labels and inputs with transparent label background
        manufacturer_label = QLabel("Manufacturer", self)
        manufacturer_label.setStyleSheet(label_style)
        self.form_layout.addRow(manufacturer_label, self.manufacturer_input)

        nickname_label = QLabel("Nickname", self)
        nickname_label.setStyleSheet(label_style)
        self.form_layout.addRow(nickname_label, self.nickname_input)

        year_label = QLabel("Year of Manufacture", self)
        year_label.setStyleSheet(label_style)
        self.form_layout.addRow(year_label, self.year_input)

        image_url_label = QLabel("Image URL", self)
        image_url_label.setStyleSheet(label_style)
        self.form_layout.addRow(image_url_label, self.image_url_input)

        chairs_label = QLabel("Number Of Chairs", self)
        chairs_label.setStyleSheet(label_style)
        self.form_layout.addRow(chairs_label, self.number_of_chairs_input)

        # Add the form layout to the container
        container_layout.addLayout(self.form_layout)

        container_layout.setSpacing(20)  # Remove the spacing between the form and other elements

        # Submit button
        self.submit_button = QPushButton("Add Aircraft", self)
        self.submit_button.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; border-radius: 10px;")
        self.submit_button.clicked.connect(self.submit_aircraft)
        container_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        # Message label for errors or success
        self.message_label = QLabel("")
        self.message_label.setStyleSheet(label_style)
        self.message_label.hide()  # Initially hide the label
        container_layout.addWidget(self.message_label, alignment=Qt.AlignCenter)

        # Set the layout for the container and add it to the main layout
        container.setLayout(container_layout)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)

        # Set the main layout
        self.setLayout(main_layout)

    def paintEvent(self, event):
        """ Custom paint event to add the background image with a dark overlay. """
        painter = QPainter(self)

        # Load the background image
        pixmap = QPixmap(r"Flight_View/icons/backgroundSky.png")  # Replace with the correct path

        # Draw the background image
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)

        # Add a semi-transparent dark overlay to darken the background
        painter.setBrush(Qt.black)
        painter.setOpacity(0.2)  # Adjust opacity to make it darker
        painter.drawRect(self.rect())

    def submit_aircraft(self):
        """Handle the submission of the aircraft form."""
        manufacturer = self.manufacturer_input.text().strip()
        nickname = self.nickname_input.text().strip()
        year_of_manufacture = self.year_input.text().strip()
        image_url = self.image_url_input.text().strip()
        number_of_chairs = self.number_of_chairs_input.text().strip()

        if not manufacturer or not nickname or not year_of_manufacture or not image_url:
            self.message_label.setText("All fields are required.")
            self.message_label.setStyleSheet("color: red;")
            self.message_label.show()
            return

        # Pass the aircraft data to the controller to save
        self.controller.save_aircraft(manufacturer, nickname, year_of_manufacture, image_url, number_of_chairs)

    def show_message(self, message, color="red"):
        """Displays success or error messages to the user."""
        if message:
            self.message_label.setText(message)
            self.message_label.setStyleSheet(f"color: {color};")
            self.message_label.show()  # Show the label when there is a message
        else:
            self.message_label.hide()  # Hide the label if no message
        
        # Trigger a layout update to resize the container
        self.adjustSize()