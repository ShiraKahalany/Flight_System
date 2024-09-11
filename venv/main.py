from PySide6.QtWidgets import QApplication
from controllers.main_controller import MainController
from dal.api_client import APIClient
from dal.dal_factory import DALFactory

def main():
    api_client = APIClient()
    dal = DALFactory(api_client)
    app = QApplication([])
    controller = MainController(dal)
    controller.show_main_window()
    app.exec_()

if __name__ == "__main__":
    main()
