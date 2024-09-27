from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QFrame, QHeaderView
from PySide6.QtGui import QPixmap, QIcon, QPainter
from PySide6.QtCore import Qt, QSize

class ManagerFlightsView(QWidget):
    def _init_(self, controller=None, flights=None):
        super()._init_()
        self.controller = controller
        self.flights = flights
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton(self)
        self.back_button.setIcon(QIcon(r"Flight_View/icons/back.png"))
        self.back_button.setIconSize(QSize(20, 20)) 

        self.back_button.setStyleSheet("""
            background-color: white; 
            border-radius: 18px;  
            border: 2px solid #3498db;  
            min-width: 36px;
            min-height: 36px;
            max-width: 36px;
            max-height: 36px;
        """)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Create a semi-transparent container for the table
        container = QFrame(self)
        container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.8);  
            border-radius: 20px;
            padding: 20px;
        """)
        container.setFixedWidth(1100)  
        container.setFixedHeight(600)

        container_layout = QVBoxLayout()

        # Title label for the page
        self.label = QLabel(f"All Flights", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 50px; 
            font-weight: bold;
            color: #000066;
            background-color: transparent;
            padding: 10px;
        """)
        container_layout.addWidget(self.label)

        # Create a table to display flights
        self.table = QTableWidget(self)
        self.table.setRowCount(len(self.flights))
        self.table.setColumnCount(8)  # 8 columns, excluding "Action"
        self.table.setHorizontalHeaderLabels(["Aircraft Image", "ID", "Aircraft", "Source", "Destination", "Departure", "Landing", "Price"])

        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setStyleSheet("font-weight: bold; font-size: 11px; background-color: #3498db; color: #3498db; padding: 2px;")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)  # Hide the vertical header

        self.table.setContentsMargins(0, 100, 0, 100)
        self.table.setStyleSheet("""
            QTableWidget::item {
                padding: 0px;
                text-align: center;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget {
                gridline-color: #3498db;
                background-color: white;
                alternate-background-color: #ecf0f1;
            }
        """)

        # Populate the table with flight data, without the Action column
        for row, flight in enumerate(self.flights):
            if flight.aircraft:
                image_label = QLabel()
                if flight.aircraft.image_data:
                    pixmap = QPixmap()
                    pixmap.loadFromData(flight.aircraft.image_data)
                    pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio)
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("No Image")

                self.table.setCellWidget(row, 0, image_label)

            self.table.setItem(row, 1, QTableWidgetItem(str(flight.id)))
            self.table.setItem(row, 2, QTableWidgetItem(flight.aircraft.nickname if flight.aircraft else "Unknown"))
            self.table.setItem(row, 3, QTableWidgetItem(flight.source))
            self.table.setItem(row, 4, QTableWidgetItem(flight.destination))
            self.table.setItem(row, 5, QTableWidgetItem(flight.departure_datetime.strftime('%Y-%m-%d %H:%M')))
            self.table.setItem(row, 6, QTableWidgetItem(flight.landing_datetime.strftime('%Y-%m-%d %H:%M')))
            self.table.setItem(row, 7, QTableWidgetItem(f"${flight.price}"))

            self.table.setRowHeight(row, 60)  # Set the row height to 60

        container_layout.addWidget(self.table)
        layout.addWidget(container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        container.setLayout(container_layout)
        self.setLayout(layout)

    def go_back(self):
        """ Calls go_back from the main application window """
        if self.parent() and hasattr(self.parent(), 'go_back'):
            self.parent().go_back()

    def paintEvent(self, event):
        """ Custom paint event to add the background image. """
        painter = QPainter(self)
        pixmap = QPixmap(r"Flight_View/icons/backgroundSky.png")  # Replace with the correct path
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)
        else:
            print("Image could not be loaded.")