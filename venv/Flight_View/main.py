import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication, QMainWindow
from controllers.login_controller import LoginController
from controllers.admin_controller import AdminController
from controllers.passenger_controller import PassengerController
from dal.interfaces.idal import IDAL

class MainApp(QMainWindow):
    def __init__(self, dal: IDAL):
        super().__init__()
        self.setWindowTitle("Flight System")
        self.setGeometry(100, 100, 800, 600)
        self.view_history = []  # Stack to track navigation history

        # Initialize AdminController and PassengerController
        self.admin_controller = AdminController(self, dal)
        self.passenger_controller = PassengerController(self, dal)

        # Pass both controllers to LoginController
        self.login_controller = LoginController(self, self.admin_controller, self.passenger_controller, dal)

        # Show login view on start
        self.show_login()

    def show_login(self):
        self.login_controller.show_login()

    def set_view(self, view):
        """ Replace the current view with the new one in the same window """
        if self.centralWidget():
            self.view_history.append(self.centralWidget())
            self.centralWidget().setParent(None)
        self.setCentralWidget(view)

    def go_back(self):
        """ Navigate back to the previous view, recreating the last view if needed """
        if self.view_history:
            previous_view = self.view_history.pop()
            # Recreate the view if necessary before setting it
            if isinstance(previous_view, LoginController):
                self.show_login()
            elif isinstance(previous_view, AdminController):
                self.admin_controller.show_admin_view()
            elif isinstance(previous_view, PassengerController):
                self.passenger_controller.show_passenger_view()
            else:
                self.setCentralWidget(previous_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())
