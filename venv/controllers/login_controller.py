#from views.login_view import LoginView
from dal.interfaces.idal import IDAL

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
            user = self.dal.User.get_user_by_credentials(username, password)
            if user:
                if user.role == "admin":
                    self.main_controller.show_admin_view()
                else:
                    self.main_controller.show_passenger_view()
                self.login_view.close()
            else:
                self.login_view.show_error("Invalid username or password")
        except Exception as e:
            self.login_view.show_error(str(e))
