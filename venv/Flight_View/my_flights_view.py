from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout, QPushButton
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from Flight_View.mock_data import tickets, flights


class MyFlightsView(QWidget):
    def __init__(self, controller=None, user_id=None):
        super().__init__()
        self.controller = controller
        self.user_id = user_id
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

        # Filter tickets by the current user's ID
        user_tickets = [t for t in tickets if t.user_id == self.user_id]

        for ticket in user_tickets:
            flight = next((f for f in flights if f.id == ticket.flight_id), None)
            if flight:
                aircraft = self.controller.get_aircraft_by_id(flight.aircraft_id)
                if aircraft:
                    flight_frame = QFrame(self)
                    flight_frame.setFrameShape(QFrame.Box)
                    flight_frame.setStyleSheet(
                        "background-color: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);")
                    flight_layout = QHBoxLayout()

                    # Aircraft Image
                    image_label = QLabel(self)
                    image_data = self.controller.download_image(aircraft.image_url)
                    if image_data:
                        pixmap = QPixmap()
                        pixmap.loadFromData(image_data)  # Load image from binary data
                        pixmap = pixmap.scaled(120, 80, Qt.KeepAspectRatio)  # Reduce size of the image
                        image_label.setPixmap(pixmap)
                    flight_layout.addWidget(image_label)

                    # Flight and ticket details
                    details_layout = QVBoxLayout()

                    # Using custom fonts and labels for a more modern look
                    flight_id_label = QLabel(f"Flight ID: {flight.id}", self)
                    flight_id_label.setFont(QFont("Arial", 10, QFont.Bold))
                    source_label = QLabel(f"Source: {flight.source}", self)
                    destination_label = QLabel(f"Destination: {flight.destination}", self)
                    departure_label = QLabel(f"Departure: {flight.departure_datetime.strftime('%Y-%m-%d %H:%M')}", self)
                    landing_label = QLabel(f"Landing: {flight.landing_datetime.strftime('%Y-%m-%d %H:%M')}", self)
                    purchase_label = QLabel(f"Purchased On: {ticket.purchase_datetime.strftime('%Y-%m-%d %H:%M')}", self)

                    details_layout.addWidget(flight_id_label)
                    details_layout.addWidget(source_label)
                    details_layout.addWidget(destination_label)
                    details_layout.addWidget(departure_label)
                    details_layout.addWidget(landing_label)
                    details_layout.addWidget(purchase_label)

                    # Styling for the text elements
                    for label in details_layout.children():
                        label.setStyleSheet("color: #34495e; padding: 2px;")

                    flight_layout.addLayout(details_layout)
                    flight_frame.setLayout(flight_layout)
                    scroll_layout.addWidget(flight_frame)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        layout.addWidget(scroll_area)
        self.setLayout(layout)
