from PySide6.QtWidgets import QMessageBox
from Flight_View.manager_view import ManagerView
from Flight_View.add_aircraft_view import AddAircraftView
from Flight_View.mock_data import aircrafts
from models.aircraft import Aircraft
from dal.interfaces.idal import IDAL

class AdminController:
    def __init__(self, main_controller, dal: IDAL):
        self.main_controller = main_controller
        self.dal=dal

    def show_admin_view(self):
        # Recreate ManagerView each time it's needed
        self.manager_view = ManagerView(controller=self)
        self.main_controller.set_view(self.manager_view)  # Set the view in the main window

    def go_back(self):
        self.main_controller.go_back()  # Handle navigation

    def add_aircraft(self):
        """Show the AddAircraftView for adding a new aircraft."""
        self.add_aircraft_view = AddAircraftView(controller=self)
        self.main_controller.set_view(self.add_aircraft_view)

    def save_aircraft(self, manufacturer, nickname, year_of_manufacture, image_url):
        """Save new aircraft data."""
        try:
            # Validate year of manufacture
            year = int(year_of_manufacture)

            # Create new aircraft object
            # new_aircraft = Aircraft(
            #     manufacturer=manufacturer,
            #     nickname=nickname,
            #     year_of_manufacture=year,
            #     image_url=image_url
            # )

            new_aircraft = {
                "manufacturer": manufacturer,
                "nickname": nickname,
                "YearOfManufacture": year_of_manufacture,
                "ImageUrl": image_url,
                "NumberOfChairs": 400
            }

            self.dal.Aircraft.create_aircraft(new_aircraft)


            # Add the aircraft to the mock data
            aircrafts.append(new_aircraft)

            # Print the newly created Aircraft object
            print(f"New aircraft created: {new_aircraft}")

            # Show success message in an alert
            self.show_success_message(f"Aircraft added successfully!\n{new_aircraft}")
        except ValueError:
            print("Invalid input for the year of manufacture.")

    def show_success_message(self, message):
        """Show a pop-up success message."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Success")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.buttonClicked.connect(self.go_back)  # Go back to admin view when "OK" is clicked
        msg_box.exec()

    def add_flight(self):
            pass