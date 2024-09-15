from Flight_View.login_view import LoginView
from Flight_View.mock_data import users

class LoginController:
    def __init__(self, main_controller, admin_controller, passenger_controller):
        self.main_controller = main_controller
        self.admin_controller = admin_controller
        self.passenger_controller = passenger_controller
        self.login_view = LoginView(self)

    def login(self, username, password):
        user = next((u for u in users if u['username'] == username and u['password_hash'] == password), None)
        if user:
            if user['role'] == 'admin':
                self.admin_controller.show_admin_view()
            else:
                self.passenger_controller.show_passenger_view()
        else:
            self.login_view.show_error("Invalid username or password")

    def show_login(self):
        self.main_controller.set_view(self.login_view)  # Set the login view in the main window
