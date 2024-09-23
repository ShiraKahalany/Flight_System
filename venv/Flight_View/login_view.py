from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout()

        # Load and display the logo
        self.logo_label = QLabel(self)

        # Ensure correct path for the image file
        logo_path = "venv/Flight_View/logo.jpg"  # Adjust this to the correct file path if it's not in the current directory

        # Check if the pixmap loads the image correctly
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            # Scale the image to a fixed size (you can adjust the width and height as needed)
            pixmap = pixmap.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Example size
            self.logo_label.setPixmap(pixmap)
        else:
            # Fallback to text if image can't be loaded
            self.logo_label.setText("Logo could not be loaded.")
            self.logo_label.setStyleSheet("color: red;")

        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Username input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #bdc3c7;")
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #bdc3c7;")
        layout.addWidget(self.password_input)

        # Connect returnPressed signal to the login function
        self.username_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)

        # Login button
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet(
            """
            background-color: #3498db; 
            color: white; 
            padding: 10px; 
            font-size: 16px; 
            border-radius: 5px; 
            margin-top: 10px;
            """
        )
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Error message label
        self.error_label = QLabel("", self)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")  # Light background

    def resizeEvent(self, event):
        """ Override resize event to adjust the logo size when the window is resized. """
        logo_path = "venv/Flight_View/logo.jpg"  # Adjust this to the correct file path if necessary
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(700, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Keep the logo size smaller
            self.logo_label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)

    def login(self):
        """Handles the login button click event."""
        username = self.username_input.text()
        password = self.password_input.text()
        self.controller.login(username, password)

    def show_error(self, message):
        """Displays error messages to the user."""
        self.error_label.setText(message)
