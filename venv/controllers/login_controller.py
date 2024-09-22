from Flight_View.login_view import LoginView
from dal.interfaces.idal import IDAL

class LoginController:
    def __init__(self, main_controller, admin_controller, passenger_controller, dal: IDAL):
        self.main_controller = main_controller
        self.admin_controller = admin_controller
        self.passenger_controller = passenger_controller
        self.dal = dal  # Store reference to the DAL
        self.login_view = LoginView(self)

    def login(self, username, password):
        """Attempts to log in the user by interacting with the DAL."""
        try:
            # Call DAL to attempt login
            user = self.dal.User.login_user(username, password)

            if user:
                # Assuming the user is an object, not a dictionary
                self.passenger_controller.current_user_id = user.id  # Access user attributes via dot notation

                # Check if the user is an admin
                if user.role == 'admin':
                    self.admin_controller.show_admin_view()
                else:
                    self.passenger_controller.show_passenger_view()
            else:
                self.login_view.show_error("Invalid username or password")
        except Exception as e:
            # Handle any errors that occur during login, e.g., DAL connection issues
            self.login_view.show_error(f"Login failed: {str(e)}")

    def show_login(self):
        """Displays the login view."""
        self.main_controller.set_view(self.login_view)
