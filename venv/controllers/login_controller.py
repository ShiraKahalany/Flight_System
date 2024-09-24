
from Flight_View.login_view import LoginView
from dal.interfaces.idal import IDAL
from exceptions import UserNotFoundException, InvalidCredentialsException, NetworkException, UnexpectedErrorException

class LoginController:
    def __init__(self, main_controller, admin_controller, passenger_controller, dal: IDAL):
        self.main_controller = main_controller
        self.admin_controller = admin_controller
        self.passenger_controller = passenger_controller
        self.dal = dal
        self.login_view = LoginView(self)

    def validate_login_input(self, username, password):
        errors = []
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        return errors

    def login(self, username, password):
        """Attempts to log in the user by interacting with the DAL."""
        errors = self.validate_login_input(username, password)
        if errors:
            self.login_view.show_error("\n".join(errors))
            return

        try:
            user = self.dal.User.login_user(username, password)

            if user:
                self.passenger_controller.current_user_id = user.id

                if user.role == 'admin':
                    self.admin_controller.show_admin_view()
                else:
                    self.passenger_controller.show_passenger_view()
            else:
                self.login_view.show_error("Invalid username or password.")

        except UserNotFoundException:
            self.login_view.show_error("User not found. Please check your username and try again.")
        except InvalidCredentialsException:
            self.login_view.show_error("Invalid username or password. Please try again.")
        except NetworkException:
            self.login_view.show_error("Network error occurred. Please check your internet connection and try again.")
        except UnexpectedErrorException as uee:
            self.login_view.show_error("An unexpected error occurred. Please try again later or contact support.")
            print(f"Unexpected error during login: {uee}")
        except Exception as e:
            self.login_view.show_error("An error occurred during login. Please try again later.")
            print(f"Unhandled exception during login: {e}")

    def show_login(self):
        """Displays the login view."""
        self.main_controller.set_view(self.login_view)