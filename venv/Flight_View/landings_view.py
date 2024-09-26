import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QFrame, QHeaderView
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtCore import Qt, QSize

class LandingsView(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller  # Pass the controller to access logic

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)  # Adjust to make it more compact

        # "Go Back" Button
        self.back_button = QPushButton(self)
        self.back_button.setIcon(QIcon(r"Flight_View/icons/back.png"))  # Replace with actual path to your icon
        self.back_button.setIconSize(QSize(20, 20))  # Adjust icon size as needed

        # Apply styles to make the button circular
        self.back_button.setStyleSheet("""
            background-color: white; 
            border-radius: 18px;  /* Circular button */
            border: 2px solid #3498db;  /* Blue border */
            min-width: 36px;
            min-height: 36px;
            max-width: 36px;
            max-height: 36px;
        """)
        self.back_button.clicked.connect(self.controller.go_back)
        main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        

        # Container for combo box and table (semi-transparent white)
        container = QFrame(self)
        container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.8);  /* Semi-transparent white */
            border-radius: 20px;
            padding: 20px;
        """)
        container.setFixedWidth(800)  # Set width for the container
        container_layout = QVBoxLayout()
        self.label = QLabel(f"All landings", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 60px; 
            font-weight: bold;
            color: #000066;
            background-color: transparent;  /* Transparent background */
            padding: 10px;  /* Adjust padding to reduce vertical space */
        """)
        container_layout.addWidget(self.label)
        # Dropdown to select hours ahead (1 to 5) with 1 hour selected by default
        self.time_dropdown = QComboBox(self)
        self.time_dropdown.addItems(['1 hour', '2 hours', '3 hours', '4 hours', '5 hours'])
        self.time_dropdown.setCurrentIndex(0)  # Set default to 1 hour
        self.time_dropdown.setStyleSheet("""
            QComboBox {
                padding: 10px;
                font-size: 16px;
                background-color: white;
                border: 2px solid #3498db;  /* Blue border */
                border-radius: 10px;
            }
        """)
        self.time_dropdown.currentIndexChanged.connect(self.update_landings)
        container_layout.addWidget(self.time_dropdown)

        # Label to show "No Landings" message
        self.no_landings_label = QLabel(self)
        self.no_landings_label.setStyleSheet("""
            color: #3498db;
            font-size: 18px;
            font-weight: bold;
        """)
        self.no_landings_label.setAlignment(Qt.AlignCenter)
        self.no_landings_label.hide()  # Hidden initially

        # Create a table to display landings with images and predictions
        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(6)  # Add a column for the Landing Prediction
        self.table.setHorizontalHeaderLabels(["Flight ID", "Source", "Destination", "Departure", "Landing", "Prediction"])

        # Set column widths and make headers visible
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setStyleSheet("font-weight: bold; font-size: 11px; background-color: #3498db; color: white; padding: 0px;")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)  # Hide the vertical header

        # Ensure padding/margins do not cut off headers
        self.table.setContentsMargins(0, 10, 0, 10)
        self.table.setStyleSheet("""
            QTableWidget::item {
                padding: 10px;
                text-align: center;  /* Center align text */
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

        # Enable alternating row colors for better readability
        self.table.setAlternatingRowColors(True)

        # Add table and message label to the container layout
        container_layout.addWidget(self.no_landings_label)  # Will be shown only when no flights
        container_layout.addWidget(self.table)  # Add table to the layout

        # Set the container layout and add to the main layout
        container.setLayout(container_layout)
        main_layout.addWidget(container, alignment=Qt.AlignTop | Qt.AlignHCenter)

        self.setLayout(main_layout)

        # Call the update_landings function when the view is first shown
        self.update_landings()

    def update_landings(self):
        """Update the landing flights table based on the hours ahead selected."""
        hours_ahead = int(self.time_dropdown.currentText().split()[0])

        # Use controller to get the upcoming landings based on the selected hours
        filtered_flights = self.controller.get_upcoming_landings(hours_ahead)

        # Clear the table and hide the "no landings" label initially
        self.table.setRowCount(0)
        self.no_landings_label.hide()

        # If there are no flights, show the message and hide the table
        if not filtered_flights:
            self.table.hide()  # Hide the table
            self.no_landings_label.setText(f"No landings in the next {hours_ahead} hours.")
            self.no_landings_label.show()  # Show the no landings message
            return

        # Otherwise, populate the table with the flight data and show it
        self.table.setRowCount(len(filtered_flights))
        self.table.show()  # Ensure the table is visible
        self.no_landings_label.hide()  # Hide the message

        # Populate the table with filtered flight data
        for row, flight in enumerate(filtered_flights):
            self.table.setItem(row, 0, self.centered_item(str(flight.id)))
            self.table.setItem(row, 1, self.centered_item(flight.source))
            self.table.setItem(row, 2, self.centered_item(flight.destination))
            self.table.setItem(row, 3, self.centered_item(flight.departure_datetime.strftime('%Y-%m-%d %H:%M')))
            self.table.setItem(row, 4, self.centered_item(flight.landing_datetime.strftime('%Y-%m-%d %H:%M')))

            # Get prediction for landing delay
            is_landing_delayed = self.controller.predict_landing_delay(flight)
            prediction_text = "Delayed" if is_landing_delayed else "On Time"
            self.table.setItem(row, 5, self.centered_item(prediction_text))

    def centered_item(self, text):
        """Helper function to create a centered QTableWidgetItem"""
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)  # Aligns text to the center
        return item

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
