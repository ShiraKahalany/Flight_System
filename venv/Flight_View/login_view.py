from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
from PySide6.QtGui import QPainter, QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, QEvent, QEvent

from PySide6.QtCore import Qt

class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Main layout for the page
        main_layout = QVBoxLayout()
        icon_label = QLabel(self)
        pixmap = QPixmap(r"Flight_View\icons\logo2.png")  # Use your provided icon path here
        icon_label.setPixmap(pixmap.scaled(600, 280))  # Adjust icon size
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("background-color: rgba(255, 255, 255, 0);")  # Fully transparent background

        # Add the icon at the top of the main layout
        main_layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Create a frame to act as a semi-transparent rectangle container
        container = QFrame(self)
        container_layout = QVBoxLayout()

        # Set the container's style (semi-transparent white background, rounded corners)
        container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.05);  /* Semi-transparent white */
            border-radius: 20px;  /* Rounded corners */
            padding: 20px;
        """)
        container_layout.addSpacing(10)

        # Username input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedWidth(300)  # Set a fixed width for the text input
        self.username_input.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #bdc3c7;")
        container_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)  # Set a fixed width for the text input
        self.password_input.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #bdc3c7;")
        container_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # Login button
        self.login_button = QPushButton("Login", self)
        self.login_button.setFixedWidth(250)  # Make the button slightly shorter than the text inputs
        self.login_button.setStyleSheet(
            """
            background-color: #3498db; 
            color: white; 
            padding: 10px; 
            font-size: 16px; 
            border-radius: 20px; 
            margin-top: 10px;
            """
        )
        self.login_button.clicked.connect(self.login)
        container_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        container_layout.addSpacing(10)

        # Add the form container to the main layout
        container.setLayout(container_layout)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)

        # Error message label
        self.error_label = QLabel("", self)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.error_label, alignment=Qt.AlignCenter)

        # Set main layout
        main_layout.setContentsMargins(50, 50, 50, 50)
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

    def login(self):
        """Handles the login button click event."""
        username = self.username_input.text()
        password = self.password_input.text()
        self.controller.login(username, password)

    def show_error(self, message):
        """Displays error messages to the user."""
        self.error_label.setText(message)

    def keyPressEvent(self, event):
        """Handles the Enter key press event to trigger login."""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.login()
