from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class FlightEntryView(QWidget):
    def __init__(self, controller=None, flight=None):
        super().__init__(parent=None)
        self.controller = controller
        self.flight = flight

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Go Back button
        self.back_button = QPushButton("← Go Back", self)
        self.back_button.clicked.connect(self.controller.go_back)  # Go back logic in controller
        self.back_button.setStyleSheet("""
            background-color: #3498db; 
            color: white; 
            padding: 10px; 
            font-size: 14px; 
            border-radius: 5px;
        """)
        layout.addWidget(self.back_button)
        layout.addSpacing(20)

        # Fonts for styling
        title_font = QFont("Arial", 24, QFont.Bold)  # Bigger title font
        regular_font = QFont("Arial", 14)  # Regular font for descriptions

        # Flight ID and route (e.g., "Flight 345: Tel Aviv → Madrid")
        flight_label = QLabel(f"Flight {self.flight.id}: {self.flight.source} → {self.flight.destination}")
        flight_label.setFont(title_font)
        flight_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(flight_label)

        layout.addSpacing(20)

        # Departure and landing details
        departure_label = QLabel(f"Departure: {self.flight.departure_datetime.strftime('%Y-%m-%d %H:%M')}")
        departure_label.setFont(regular_font)
        departure_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(departure_label)

        landing_label = QLabel(f"Landing: {self.flight.landing_datetime.strftime('%Y-%m-%d %H:%M')}")
        landing_label.setFont(regular_font)
        landing_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(landing_label)

        # Add space between text and credit card section
        layout.addSpacing(20)

        # Credit card details form
        credit_card_box = self.create_credit_card_box()
        layout.addWidget(credit_card_box)

        # Add space before the button
        layout.addSpacing(30)

        # "Purchase" Button - centered
        self.purchase_button = QPushButton("Purchase Ticket", self)
        self.purchase_button.clicked.connect(self.purchase_flight)
        self.purchase_button.setStyleSheet("background-color: #3498db; color: white; padding: 10px 20px; margin-top: 20px;")
        self.purchase_button.setFont(QFont("Arial", 16))
        layout.addWidget(self.purchase_button)

        # Set the layout
        self.setLayout(layout)

    def create_credit_card_box(self):
        """Create a form for credit card details inside a bordered box with a smaller width."""
        credit_box = QFrame()
        credit_box.setFrameShape(QFrame.Box)
        credit_box.setLineWidth(2)
        credit_box.setFixedWidth(400)  # Make the credit card section narrower

        credit_layout = QFormLayout()
        credit_layout.setAlignment(Qt.AlignCenter)
        credit_box.setLayout(credit_layout)

        # Credit card details input
        card_number_input = QLineEdit()
        card_number_input.setPlaceholderText("Card Number")
        card_number_input.setFont(QFont("Arial", 12))
        
        cvv_input = QLineEdit()
        cvv_input.setPlaceholderText("CVV")
        cvv_input.setFont(QFont("Arial", 12))
        cvv_input.setMaxLength(3)
        
        expiry_date_input = QLineEdit()
        expiry_date_input.setPlaceholderText("Expiry Date (MM/YY)")
        expiry_date_input.setFont(QFont("Arial", 12))

        # Add the fields to the layout
        credit_layout.addRow(QLabel("Card Number:"), card_number_input)
        credit_layout.addRow(QLabel("CVV:"), cvv_input)
        credit_layout.addRow(QLabel("Expiry Date:"), expiry_date_input)

        return credit_box

    def purchase_flight(self):
        """ Calls the controller to purchase the flight """
        self.controller.purchase_ticket(self.flight.id)
