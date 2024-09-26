from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, 
                               QHBoxLayout, QPushButton, QApplication)
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QSize

class MyFlightsView(QWidget):
    def __init__(self, controller=None, tickets=None):
        super().__init__()
        self.controller = controller
        self.tickets = tickets or []
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # "Go Back" Button
        self.back_button = QPushButton(self)
        self.back_button.setIcon(QIcon(r"Flight_View\icons\back.png"))
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
        self.back_button.clicked.connect(self.controller.go_back)
        main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Container for flight cards or message
        container = QFrame(self)
        container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 20px;
        """)
        container_layout = QVBoxLayout(container)

        if not self.tickets:
            # Display message when no tickets are available
            no_tickets_label = QLabel("You don't have any flights soon")
            no_tickets_label.setAlignment(Qt.AlignCenter)
            no_tickets_label.setStyleSheet("""
                font-family: 'Segoe UI';
                font-size: 24px;
                color: #555;
                background: transparent;
            """)
            container_layout.addWidget(no_tickets_label)
        else:
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    background: transparent;
                    border: none;
                }
                QScrollBar:vertical {
                    width: 0px;
                }
            """)

            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setSpacing(10)  # Spacing between cards

            for ticket in self.tickets:
                flight = self.controller.dal.Flight.get_flight_by_id(ticket.flight_id)
                aircraft = self.controller.dal.Aircraft.get_aircraft_by_id(flight.aircraft_id)
                if aircraft and flight:
                    ticket_frame = self.create_ticket_frame(ticket, flight)
                    scroll_layout.addWidget(ticket_frame)

            scroll_area.setWidget(scroll_content)
            container_layout.addWidget(scroll_area)

        main_layout.addWidget(container)

    def create_ticket_frame(self, ticket, flight):
        ticket_frame = QFrame()
        ticket_frame.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #e0e0e0;
        """)
        ticket_layout = QHBoxLayout(ticket_frame)
        ticket_layout.setContentsMargins(10, 5, 10, 5)  # Reduced vertical padding

        # Airplane Icon
        airplane_icon_label = QLabel()
        airplane_icon = QPixmap('Flight_View/icons/airplane.png')
        airplane_icon = airplane_icon.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        airplane_icon_label.setPixmap(airplane_icon)
        airplane_icon_label.setStyleSheet("background: transparent; border: none;")
        ticket_layout.addWidget(airplane_icon_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        # Flight Details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(2)  # Reduced spacing between text lines

        flight_id_label = QLabel(f"Flight ID: {flight.id}")
        flight_id_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        flight_id_label.setStyleSheet("background: transparent; border: none;")
        details_layout.addWidget(flight_id_label)

        for label_text in [
            f"Source: {flight.source}",
            f"Destination: {flight.destination}",
            f"Departure: {flight.departure_datetime.strftime('%Y-%m-%d %H:%M')}",
            f"Landing: {flight.landing_datetime.strftime('%Y-%m-%d %H:%M')}"
        ]:
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 10))
            label.setStyleSheet("background: transparent; border: none;")
            details_layout.addWidget(label)

        ticket_layout.addLayout(details_layout)

        # Download Button
        download_button = QPushButton()
        download_button.setIcon(QIcon('Flight_View/icons/download.png'))
        download_button.setIconSize(QSize(24, 24))  # Increased icon size
        download_button.setFixedSize(48, 48)  # Increased button size
        download_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                border-radius: 24px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        download_button.clicked.connect(lambda: self.controller.download_ticket_pdf(ticket))
        ticket_layout.addWidget(download_button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        return ticket_frame

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(r"Flight_View/icons/backgroundSky.png")
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)
        painter.setBrush(QColor(0, 0, 0, 51))  # 20% opacity black
        painter.drawRect(self.rect())

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyFlightsView()
    window.show()
    sys.exit(app.exec())