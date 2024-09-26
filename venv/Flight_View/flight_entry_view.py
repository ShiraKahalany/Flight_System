from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QPushButton, QVBoxLayout, QLineEdit, QFrame
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter

class FlightEntryView(QWidget):
    def __init__(self, controller=None, flight=None):
        super().__init__(parent=None)
        self.controller = controller
        self.flight = flight

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Go Back button
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
        self.back_button.clicked.connect(self.controller.go_back)
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Create a semi-transparent container for the content
        container = QFrame(self)
        container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.8);  
            border-radius: 20px;
            padding: 20px;
        """)
        container.setFixedWidth(700)  
        container.setFixedHeight(550)  

        container_layout = QVBoxLayout()

        # Fonts for styling
        title_font = QFont("Arial", 24, QFont.Bold)  # Bigger title font
        regular_font = QFont("Arial", 14)  # Regular font for descriptions

        # Flight ID and route (e.g., "Flight 345: Tel Aviv → Madrid")
        flight_label = QLabel(f"Flight {self.flight.id}: {self.flight.source} → {self.flight.destination}")
        flight_label.setFont(title_font)
        flight_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(flight_label)

        container_layout.addSpacing(20)

        # Departure and landing details
        departure_label = QLabel(f"Departure: {self.flight.departure_datetime.strftime('%Y-%m-%d %H:%M')}")
        departure_label.setFont(regular_font)
        departure_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(departure_label)

        landing_label = QLabel(f"Landing: {self.flight.landing_datetime.strftime('%Y-%m-%d %H:%M')}")
        landing_label.setFont(regular_font)
        landing_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(landing_label)

        container_layout.addSpacing(20)

        # Credit card details form
        credit_card_box = self.create_credit_card_box()
        container_layout.addWidget(credit_card_box, alignment=Qt.AlignCenter)

        container_layout.addSpacing(20)

        # "Purchase" Button - centered
        self.purchase_button = QPushButton("Purchase Ticket", self)
        self.purchase_button.clicked.connect(self.purchase_flight)
        self.purchase_button.setStyleSheet("""
            background-color: #3498db; 
            color: white; 
            padding: 10px 20px; 
            margin-top: 20px;
        """)
        self.purchase_button.setFont(QFont("Arial", 16))
        container_layout.addWidget(self.purchase_button, alignment=Qt.AlignCenter)

        # Add container layout to the container
        container.setLayout(container_layout)

        # Add the container to the main layout
        layout.addWidget(container, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def create_credit_card_box(self):
        """Create a form for credit card details inside a bordered box."""
        credit_box = QFrame()
        credit_box.setFrameShape(QFrame.Box)
        credit_box.setLineWidth(2)
        credit_box.setFixedWidth(450)  # Adjust width to fit inputs properly
        credit_box.setFixedHeight(200)

        credit_layout = QFormLayout()
        credit_layout.setHorizontalSpacing(5)  # Add space between labels and inputs
        credit_box.setLayout(credit_layout)

        # Credit card details input
        card_number_input = QLineEdit()
        card_number_input.setPlaceholderText("Card Number")
        card_number_input.setFont(QFont("Arial", 10))
        card_number_input.setFixedHeight(30)  # Adjust input box height
        card_number_input.setFixedWidth(250)  # Adjust input box width

        cvv_input = QLineEdit()
        cvv_input.setPlaceholderText("CVV")
        cvv_input.setFont(QFont("Arial", 10))
        cvv_input.setMaxLength(3)
        cvv_input.setFixedHeight(30)  # Adjust input box height
        cvv_input.setFixedWidth(150)  # Adjust input box width

        expiry_date_input = QLineEdit()
        expiry_date_input.setPlaceholderText("Expiry Date (MM/YY)")
        expiry_date_input.setFont(QFont("Arial", 10))
        expiry_date_input.setFixedHeight(30)  # Adjust input box height
        expiry_date_input.setFixedWidth(250)  # Adjust input box width

        # Styling labels
        label_font = QFont("Arial", 10)

        card_label = QLabel("Card Number:")
        card_label.setFixedHeight(25)
        card_label.setFont(label_font)
        cvv_label = QLabel("CVV:")
        cvv_label.setFixedHeight(25)
        cvv_label.setFont(label_font)
        expiry_label = QLabel("Expiry Date:")
        expiry_label.setFixedHeight(25)

        expiry_label.setFont(label_font)

        # Add the fields to the layout
        credit_layout.addRow(card_label, card_number_input)
        credit_layout.addRow(cvv_label, cvv_input)
        credit_layout.addRow(expiry_label, expiry_date_input)

        return credit_box

    def purchase_flight(self):
        """ Calls the controller to purchase the flight """
        self.controller.purchase_ticket(self.flight.id)

    def paintEvent(self, event):
        """ Custom paint event to add the background image. """
        painter = QPainter(self)

        # Load the background image (sky background)
        pixmap = QPixmap(r"Flight_View/icons/backgroundSky.png")  # Replace with the correct path

        # Draw the background image
        if not pixmap.isNull():
            painter.drawPixmap(self.rect(), pixmap)
        else:
            print("Image could not be loaded.")
