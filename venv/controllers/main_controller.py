#from views.main_window import MainWindow
from controllers.login_controller import LoginController
from controllers.admin_controller import AdminController
from controllers.passenger_controller import PassengerController
from dal.interfaces.idal import IDAL

class MainController:
    def __init__(self, dal: IDAL):
        self.dal = dal
        self.main_window = None
        self.login_controller = LoginController(self, self.dal)
        self.admin_controller = AdminController(self, self.dal)
        self.passenger_controller = PassengerController(self, self.dal)

    def show_main_window(self):
       # self.main_window = MainWindow(self)
        self.main_window.show()

    def show_login(self):
        self.login_controller.show_login()

    def show_admin_view(self):
        self.admin_controller.show_admin_view()

    def show_passenger_view(self):
        self.passenger_controller.show_passenger_view()