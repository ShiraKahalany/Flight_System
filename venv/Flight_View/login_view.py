from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class LoginView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout()

        self.label = QLabel("Login", self)
        layout.addWidget(self.label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)  # Logic in controller
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.controller.login(username, password)  # Delegate logic to controller

    def show_error(self, message):
        self.label.setText(message)
