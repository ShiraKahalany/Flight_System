from PySide6.QtWidgets import QMessageBox, QFileDialog
from Flight_View.my_flights_view import MyFlightsView
from exceptions import TicketRetrievalException, NetworkException, UnexpectedErrorException
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class MyFlightsController:
    def __init__(self, main_controller, dal):
        self.main_controller = main_controller
        self.dal = dal
        self.current_user_id = None

    def show_my_flights(self, user_id):
        try:
            tickets = self.dal.Ticket.get_user_tickets(user_id)
            my_flights_view = MyFlightsView(controller=self, tickets=tickets)
            self.main_controller.set_view(my_flights_view)
        except TicketRetrievalException as tre:
            self.show_error_message(f"Unable to retrieve your flights: {tre}")
        except NetworkException as ne:
            self.show_error_message(f"Network error while fetching your flights: {ne}")
        except UnexpectedErrorException as uee:
            self.show_error_message("An unexpected error occurred. Please try again later.")
        except Exception as e:
            self.show_error_message("An error occurred while loading your flights. Please try again.")

    def download_ticket_pdf(self, ticket):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options
        )
        
        if not file_path:
            return  # User canceled the file dialog

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        pdf = SimpleDocTemplate(file_path, pagesize=letter)
        content = []

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.fontSize = 20
        title_style.alignment = 1  # Center alignment
        
        normal_style = ParagraphStyle(
            name='Normal',
            fontSize=12,
            leading=14,
            alignment=1  # Centered text
        )

        label_style = ParagraphStyle(
            name='Label',
            fontSize=10,
            leading=12,
            textColor='gray',
            alignment=1  # Centered text
        )

        icon_path = os.path.join(os.path.dirname(__file__), '..', 'Flight_View', 'icons', 'ticket.png')
        if os.path.exists(icon_path):
            content.append(Image(icon_path, 1.5 * inch, 1.5 * inch))
        else:
            print(f"Error: Icon file not found at {icon_path}")

        content.append(Paragraph(f"Flight Ticket: {ticket.id}", title_style))
        content.append(Spacer(1, 12))

        flight = self.dal.Flight.get_flight_by_id(ticket.flight_id)
        aircraft = self.dal.Aircraft.get_aircraft_by_id(flight.aircraft_id)
        
        details = [
            {"label": "Flight", "value": f"{flight.source} → {flight.destination}"},
            {"label": "Departure", "value": flight.departure_datetime.strftime('%Y-%m-%d %H:%M')},
            {"label": "Landing", "value": flight.landing_datetime.strftime('%Y-%m-%d %H:%M')},
            {"label": "Aircraft", "value": aircraft.nickname},
            {"label": "Purchase time", "value": ticket.purchase_datetime.strftime('%Y-%m-%d %H:%M')}
        ]

        for detail in details:
            content.append(Paragraph(detail["label"], label_style))
            content.append(Paragraph(detail["value"], normal_style))
            content.append(Spacer(1, 10))

        pdf.build(content)

        print(f"PDF saved: {file_path}")
        os.startfile(file_path)  # This will open the file automatically on Windows.

    def show_error_message(self, message):
        QMessageBox.critical(None, "Error", message, QMessageBox.Ok)

    def show_success_message(self, message):
        QMessageBox.information(None, "Success", message, QMessageBox.Ok)
        
    def set_current_user(self, user_id):
        self.current_user_id = user_id
        
    def go_back(self):
        self.main_controller.go_back()