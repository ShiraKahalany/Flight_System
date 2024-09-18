import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from controllers.main_controller import MainController
from dal.api_client import APIClient
from dal.dal_factory import DALFactory
from Flight_View.main import MainApp

# def main():
#     api_client = APIClient()
#     dal = DALFactory(api_client)
#     app = QApplication([])
#     controller = MainController(dal)
#     controller.show_main_window()
#     app.exec_()

if __name__ == "__main__":
    dal= DALFactory.get_instance()
    app = QApplication(sys.argv)
    main_window = MainApp(dal)
    main_window.show()
    sys.exit(app.exec())
    #main()
