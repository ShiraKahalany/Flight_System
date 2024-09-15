import sys
from PySide6.QtWidgets import QApplication, QMainWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flight System")
        self.setGeometry(100, 100, 800, 600)
        self.view_history = []  # Stack to track navigation history
        self.show_login()

    def show_login(self):
        from login_view import LoginView
        self.set_view(LoginView(self))

    def show_passenger_dashboard(self, user):
        from frequent_flyer_view import FrequentFlyerView
        self.set_view(FrequentFlyerView(self, user))

    def show_admin_dashboard(self, user):
        from manager_view import ManagerView
        self.set_view(ManagerView(self, user))

    def set_view(self, view):
        """ Set the current view and add the previous one to the history """
        if self.centralWidget():
            self.view_history.append(self.centralWidget())
            self.centralWidget().setParent(None)  # Prevent automatic deletion
        self.setCentralWidget(view)

    def go_back(self):
        """ Go back to the previous view """
        if self.view_history:
            previous_view = self.view_history.pop()
            self.setCentralWidget(previous_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())
