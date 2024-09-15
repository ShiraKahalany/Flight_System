
from venv.dal.dal_impl import DALImpl
from venv.dal.interfaces.idal import IDAL
from datetime import datetime, timedelta
import logging
from venv.dal.api_client import APIClient
from venv.dal.dal_factory import DALFactory

# Set up logging - this will print to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_date_checker(dal):
    logger.info("Testing DateChecker")
    date_checker = dal.DateDetails

    date = datetime.now()
    location = "Jerusalem"
    departure = datetime.now()
    arrival = departure + timedelta(hours=5)
    departure_location = "Tel Aviv"
    arrival_location = "New York"

    logger.info(date_checker.get_date_details(date, location))
    """
    logger.info(date_checker.is_flight_allowed(departure, arrival, departure_location, arrival_location))
    logger.info(date_checker.get_flight_warnings(departure, arrival, departure_location, arrival_location))
    logger.info(date_checker.get_shabbat_times(date, location))
    logger.info(date_checker.get_parasha(date, location))
    """

"""

def test_user_dal(dal):
    logger.info("Testing UserDAL")
    user_dal = dal.User

    # Assuming these methods exist. Adjust as necessary.
    new_user = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
    created_user = user_dal.create_user(new_user)
    logger.info(f"Created user: {created_user}")

    user = user_dal.get_user(created_user['id'])
    logger.info(f"Retrieved user: {user}")

    user_dal.update_user(created_user['id'], {"email": "newemail@example.com"})
    updated_user = user_dal.get_user(created_user['id'])
    logger.info(f"Updated user: {updated_user}")

    user_dal.delete_user(created_user['id'])
    logger.info("User deleted")

def test_flight_dal(dal):
    logger.info("Testing FlightDAL")
    flight_dal = dal.Flight

    # Assuming these methods exist. Adjust as necessary.
    new_flight = {
        "flight_number": "FL123",
        "departure": "Tel Aviv",
        "arrival": "New York",
        "departure_time": datetime.now() + timedelta(days=1),
        "arrival_time": datetime.now() + timedelta(days=1, hours=12)
    }
    created_flight = flight_dal.create_flight(new_flight)
    logger.info(f"Created flight: {created_flight}")

    flight = flight_dal.get_flight(created_flight['id'])
    logger.info(f"Retrieved flight: {flight}")

    flight_dal.update_flight(created_flight['id'], {"arrival": "Los Angeles"})
    updated_flight = flight_dal.get_flight(created_flight['id'])
    logger.info(f"Updated flight: {updated_flight}")

    flight_dal.delete_flight(created_flight['id'])
    logger.info("Flight deleted")

def test_aircraft_dal(dal):
    logger.info("Testing AircraftDAL")
    aircraft_dal = dal.Aircraft

    # Assuming these methods exist. Adjust as necessary.
    new_aircraft = {
        "model": "Boeing 747",
        "capacity": 366,
        "manufacturer": "Boeing"
    }
    created_aircraft = aircraft_dal.create_aircraft(new_aircraft)
    logger.info(f"Created aircraft: {created_aircraft}")

    aircraft = aircraft_dal.get_aircraft(created_aircraft['id'])
    logger.info(f"Retrieved aircraft: {aircraft}")

    aircraft_dal.update_aircraft(created_aircraft['id'], {"capacity": 400})
    updated_aircraft = aircraft_dal.get_aircraft(created_aircraft['id'])
    logger.info(f"Updated aircraft: {updated_aircraft}")

    aircraft_dal.delete_aircraft(created_aircraft['id'])
    logger.info("Aircraft deleted")

def test_ticket_dal(dal):
    logger.info("Testing TicketDAL")
    ticket_dal = dal.Ticket

    # Assuming these methods exist. Adjust as necessary.
    new_ticket = {
        "flight_id": "FL123",
        "user_id": "USER456",
        "seat_number": "12A"
    }
    created_ticket = ticket_dal.create_ticket(new_ticket)
    logger.info(f"Created ticket: {created_ticket}")

    ticket = ticket_dal.get_ticket(created_ticket['id'])
    logger.info(f"Retrieved ticket: {ticket}")

    ticket_dal.update_ticket(created_ticket['id'], {"seat_number": "14B"})
    updated_ticket = ticket_dal.get_ticket(created_ticket['id'])
    logger.info(f"Updated ticket: {updated_ticket}")

    ticket_dal.delete_ticket(created_ticket['id'])
    logger.info("Ticket deleted")

"""


def main():

    api_client = APIClient()
    dal = DALFactory(api_client)
    #dal = DALImpl()

    test_date_checker(dal)
    #test_user_dal(dal)
    #test_flight_dal(dal)
    #test_aircraft_dal(dal)
    #test_ticket_dal(dal)



if __name__ == "__main__":
    main()
