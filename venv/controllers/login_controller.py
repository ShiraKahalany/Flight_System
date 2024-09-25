
from Flight_View.login_view import LoginView
from dal.interfaces.idal import IDAL
from exceptions import UserNotFoundException, InvalidCredentialsException, NetworkException, UnexpectedErrorException
from datetime import datetime, timedelta


class LoginController:
    def __init__(self, main_controller, admin_controller, passenger_controller, dal: IDAL):
        self.main_controller = main_controller
        self.admin_controller = admin_controller
        self.passenger_controller = passenger_controller
        self.dal = dal
        self.login_view = LoginView(self)
        
    def set_current_user(self, user_id):
        self.current_user_id = user_id

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
            today_details = self.dal.DateDetails.get_date_details(datetime.now(), "Tel Aviv")

            if user:
                self.passenger_controller.current_user_id = user.id
                self.passenger_controller.flight_booking_controller.set_current_user(user.id)
                self.passenger_controller.my_flights_controller.set_current_user(user.id)

                if user.role == 'admin':
                    self.admin_controller.show_admin_view(user=user)
                else:
                    self.passenger_controller.show_passenger_view(user=user, date_details=today_details)
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