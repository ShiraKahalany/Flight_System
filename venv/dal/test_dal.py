import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dal.dal_factory import DALFactory
#from interfaces.idal import IDAL 
from datetime import datetime, timedelta
import logging
from dal.api_client import APIClient
from models.aircraft import Aircraft
from models.hebrew_times import DateDetails
from models.flight import Flight
from models.user import User
from models.ticket import Ticket
#import Utils
from controllers.utils import Utils

# Set up logging - this will print to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_date_checker(dal):
    date_checker = dal.DateDetails

    date = datetime.now()
    location = "Tel Aviv"
    departure = datetime.now()
    arrival = departure + timedelta(hours=5)
    departure_location = "Tel Aviv"
    arrival_location = "Tel Aviv"

    date_details = date_checker.get_date_details(date, location)
    logger.info(f"Date parasha: {date_details.parasha}. is shabbat? {date_details.day_of_week==6}",)
    is_flight_allowed = Utils().is_flight_during_shabbat_or_holiday(departure, arrival, departure_location)
    logger.info(f"Is flight allowed? {is_flight_allowed}")

    # logger.info(date_checker.get_date_details(date, location))
    # logger.info(date_checker.is_flight_allowed(departure, arrival, departure_location, arrival_location))
    # logger.info(date_checker.get_flight_warnings(departure, arrival, departure_location, arrival_location))
    # logger.info(date_checker.get_shabbat_times(date, location))
    # logger.info(date_checker.get_parasha(date, location))


def test_user_dal(dal):
    user_dal = dal.User

    # Assuming these methods exist. Adjust as necessary.
    new_user = User(
        username= "testus8er4556",
        role= "passenger",
        first_name= "Avi",
        last_name= "Cohen",
        email= "testuser@example.com",
        password= "password123"
    )
    created_user = user_dal.create_user(new_user)
    logger.info(f"Created user: {created_user}. type: {type(created_user)}")    

    # user = user_dal.get_user(created_user['id'])
    # logger.info(f"Retrieved user: {user}")

    # user_dal.update_user(created_user['id'], {"email": "newemail@example.com"})
    # updated_user = user_dal.get_user(created_user['id'])
    # logger.info(f"Updated user: {updated_user}")

    # user_dal.delete_user(created_user['id'])
    # logger.info("User deleted")

    username = "johnsonmary"
    password = "k9GzyQXp^9"
    user = user_dal.login_user(username, password)
    logger.info(f"Logged in user: {user.role}")

def test_flight_dal(dal):
    # logger.info("Testing FlightDAL")
    flight_dal = dal.Flight

    # Assuming these methods exist. Adjust as necessary.
    new_flight = {
        "id": "123",
        "aircraft_id": "1054",
        "source": "Tel Aviv",
        "destination": "New York",
        "departure_datetime": str(datetime.now() + timedelta(days=1)),
        "landing_datetime": str(datetime.now() + timedelta(days=1, hours=12)),
        "delayed_landing_time": ""
    }

    new_flight = Flight(
        aircraft_id=1022, 
        source="Tel Aviv", 
        destination="New York",
        departure_datetime=datetime.now() + timedelta(days=1),
        landing_datetime=datetime.now() + timedelta(days=1, hours=12),
        delayed_landing_time=""
    )   
    created_flight = flight_dal.create_flight(new_flight)
    # logger.info(f"Created flight id: {created_flight.id}, created flight des: {created_flight.destination}")

    # flight = flight_dal.get_flight(created_flight['id'])
    # logger.info(f"Retrieved flight: {flight}")

    # flight_dal.update_flight(created_flight['id'], {"arrival": "Los Angeles"})
    # updated_flight = flight_dal.get_flight(created_flight['id'])
    # logger.info(f"Updated flight: {updated_flight}")

    # flight_dal.delete_flight(created_flight['id'])
    # logger.info("Flight deleted")

    flights = flight_dal.get_BGR_lands_next_5_hours()
    #print each flight
    for flight in flights:
        logger.info(f"Retrieved flight: {flight.destination}")  

def test_aircraft_dal(dal):
    logger.info("Testing AircraftDAL")
    aircraft_dal = dal.Aircraft

    # Assuming these methods exist. Adjust as necessary.
    new_aircraft = {
        "manufacturer": "Boeing",
        "nickname": "Jumbo Jet",
        "YearOfManufacture": 1998,
        "ImageUrl": "https://picsum.photos/400/300",
        "NumberOfChairs": 400
    }

    aircraft_dal.create_aircraft(new_aircraft)

    # logger.info(f"Created aircraft")

    aircraft = aircraft_dal.get_aircraft(1023)
    logger.info(f"Retrieved aircraft: {aircraft}")

    # aircraft_dal.update_aircraft(created_aircraft['id'], {"capacity": 400})
    # updated_aircraft = aircraft_dal.get_aircraft(created_aircraft['id'])
    # logger.info(f"Updated aircraft: {updated_aircraft}")

    # aircraft_dal.delete_aircraft(created_aircraft['id'])
    # logger.info("Aircraft deleted")

def test_ticket_dal(dal):
    ticket_dal = dal.Ticket

    # Assuming these methods exist. Adjust as necessary.
    new_ticket = Ticket(
        flight_id= "345",
        user_id= "322361361",
        purchase_datetime= datetime.now()
    )
    created_ticket = ticket_dal.create_ticket(new_ticket)
    logger.info(f"Created ticket: {created_ticket}")

    ticket = ticket_dal.get_ticket(created_ticket['id'])
    logger.info(f"Retrieved ticket: {ticket}")

    ticket_dal.update_ticket(created_ticket['id'], {"seat_number": "14B"})
    updated_ticket = ticket_dal.get_ticket(created_ticket['id'])
    logger.info(f"Updated ticket: {updated_ticket}")

    ticket_dal.delete_ticket(created_ticket['id'])
    logger.info("Ticket deleted")


def test_image_recognition_functionality(self):
        # Test get_image_tags
        aircraft_image_url = "https://www.now14.co.il/wp-content/uploads/2023/01/shutterstock_2117654495-768x512.jpg"
        tags = self.ImageRecognition.get_image_tags(aircraft_image_url)
        print(f"tags: {tags}")
        #self.assertIsInstance(tags, list)
        #self.assertTrue(len(tags) > 0)

        #  Test is_aircraft_image with an aircraft image
        is_aircraft = self.ImageRecognition.is_aircraft_image(aircraft_image_url)
        print(f"is_aircraft????? {is_aircraft}")
        # self.assertTrue(is_aircraft)

        # # Test is_aircraft_image with a non-aircraft image
        # non_aircraft_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Dendrocygna_bicolor_wilhelma.jpg/429px-Dendrocygna_bicolor_wilhelma.jpg"
        # is_aircraft = self.dal.ImageRecognition.is_aircraft_image(non_aircraft_image_url)
        # self.assertFalse(is_aircraft)




def main():

    api_client = APIClient()
    dal = DALFactory.get_instance()
    #test_image_recognition_functionality(dal)
    #dal = DALImpl()

    #test_date_checker(dal)
    test_user_dal(dal)
    #test_flight_dal(dal)
    #test_aircraft_dal(dal)
    #test_ticket_dal(dal)



if __name__ == "__main__":
    main()
