from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout, QPushButton
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt

class MyFlightsView(QWidget):
    def __init__(self, controller=None, flights=None):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout()

        # "Go Back" Button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        self.back_button.clicked.connect(self.controller.go_back)
        layout.addWidget(self.back_button)

        # Scroll Area to hold flight tickets
        scroll_area = QScrollArea(self)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        for flight in flights:
            aircraft = self.controller.dal.Aircraft.get_aircraft_by_id(flight.aircraft_id)
            if aircraft:
                # Create a ticket frame without stylesheet
                ticket_frame = QFrame(self)
                ticket_frame.setFrameShape(QFrame.NoFrame)  # No extra frame shape
                ticket_frame.setContentsMargins(10, 10, 10, 10)  # Apply margins directly
                ticket_frame.setStyleSheet("border-bottom: 1px solid #cccccc;")  # Only minimal stylesheet
                
                ticket_layout = QHBoxLayout()

                # Airplane Icon (left side)
                airplane_icon_label = QLabel(self)
                airplane_icon = QPixmap('venv/Flight_View/icons/airplane.png')  # Verify correct path
                airplane_icon = airplane_icon.scaled(60, 60, Qt.KeepAspectRatio)
                airplane_icon_label.setPixmap(airplane_icon)
                ticket_layout.addWidget(airplane_icon_label, alignment=Qt.AlignLeft)

                # Flight and ticket details (center)
                details_layout = QVBoxLayout()
                details_layout.setSpacing(3)

                flight_id_label = QLabel(f"Flight ID: {flight.id}", self)
                flight_id_label.setFont(QFont("Arial", 10, QFont.Bold))
                source_label = QLabel(f"Source: {flight.source}", self)
                destination_label = QLabel(f"Destination: {flight.destination}", self)
                departure_label = QLabel(f"Departure: {flight.departure_datetime.strftime('%Y-%m-%d %H:%M')}", self)
                landing_label = QLabel(f"Landing: {flight.landing_datetime.strftime('%Y-%m-%d %H:%M')}", self)

                for label in [flight_id_label, source_label, destination_label, departure_label, landing_label]:
                    label.setStyleSheet("color: #333333; font-size: 12px;")

                details_layout.addWidget(flight_id_label)
                details_layout.addWidget(source_label)
                details_layout.addWidget(destination_label)
                details_layout.addWidget(departure_label)
                details_layout.addWidget(landing_label)

                ticket_layout.addLayout(details_layout)

                # Circular Download PDF Button with Icon (right side)
                download_button = QPushButton(self)
                download_button.setIcon(QIcon('venv/Flight_View/icons/download.png'))  # Ensure icon path is correct
                download_button.setFixedSize(50, 50)  # Directly set size
                download_button.setStyleSheet("background-color: #2ecc71; border-radius: 25px;")  # Apply only necessary styles
                
                download_button.clicked.connect(lambda checked, f=flight: self.controller.download_ticket_pdf(f))

                # Align the button on the right-bottom side
                ticket_layout.addWidget(download_button, alignment=Qt.AlignRight | Qt.AlignBottom)

                ticket_frame.setLayout(ticket_layout)
                scroll_layout.addWidget(ticket_frame)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        layout.addWidget(scroll_area)
        self.setLayout(layout)
