#from views.login_view import LoginView
from dal.api_client import APIClient
from dal.idal import IDAL

class LoginController:
    def __init__(self, main_controller, dal: IDAL):
        self.main_controller = main_controller
        self.dal = dal
        self.login_view = None

    def show_login(self):
        #self.login_view = LoginView(self)
        self.login_view.show()

    def login(self, username, password):
        try:
            # Assuming the API returns user data on successful login
            user_data = self.dal.create_user({"username": username, "password": password})
            if user_data.role == "admin":
                self.main_controller.show_admin_view()
            else:
                self.main_controller.show_passenger_view()
            self.login_view.close()
        except Exception as e:
            self.login_view.show_error(str(e))