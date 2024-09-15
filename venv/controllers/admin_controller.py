from Flight_View.manager_view import ManagerView

class AdminController:
    def __init__(self, main_controller):
        self.main_controller = main_controller

    def show_admin_view(self):
        # Recreate ManagerView each time it's needed
        self.manager_view = ManagerView(controller=self)
        self.main_controller.set_view(self.manager_view)  # Set the view in the main window

    def go_back(self):
        self.main_controller.go_back()  # Handle navigation

    def add_aircraft(self):
        pass

    def add_flight(self):
        pass
