import sys

from PySide6.QtWidgets import QApplication
from dal.api_client import APIClient
from dal.dal_factory import DALFactory
from Flight_View.main_app import MainApp



if __name__ == "__main__":
    dal= DALFactory.get_instance()
    app = QApplication(sys.argv)
    main_window = MainApp(dal)
    main_window.show()
    sys.exit(app.exec())

