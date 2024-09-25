import sys
import os
import json
import requests
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
from exceptions import*

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
        username= "danush",
        role= "passenger",
        first_name= "Avi",
        last_name= "Cohen",
        email= "testuser@example.com",
        password= "password123"
    )
    # created_user = user_dal.create_user(new_user)
    # logger.info(f"Created user: {created_user}. type: {type(created_user)}")

    try:
        username = "danush"
        password = "password123"
        #user = user_dal.login_user(username, password)
        created_user = user_dal.create_user(new_user)
    except UserNotFoundException:
        print('error: User not found')
    except InvalidCredentialsException:
        print("error Invalid credentials")
    except NetworkException as e:
        logger.error(f"Network error during login: {str(e)}")
        print("error Network error occurred")
    except UnexpectedErrorException as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        print("error  An unexpected error occurred")

    # user = user_dal.get_user(created_user['id'])
    # logger.info(f"Retrieved user: {user}")

    # user_dal.update_user(created_user['id'], {"email": "newemail@example.com"})
    # updated_user = user_dal.get_user(created_user['id'])
    # logger.info(f"Updated user: {updated_user}")

    # user_dal.delete_user(created_user['id'])
    # logger.info("User deleted")

    # username = "johnsonmary"
    # password = "k9GzyQXp^9"
    # user = user_dal.login_user(username, password)
    # logger.info(f"Logged in user: {user.role}")

def test_flight_dal(dal):
    # logger.info("Testing FlightDAL")
    flight_dal = dal.Flight

    # Assuming these methods exist. Adjust as necessary.
    # new_flight = {
    #     "id": "123",
    #     "aircraft_id": "1054",
    #     "source": "Tel Aviv",
    #     "destination": "New York",
    #     "departure_datetime": str(datetime.now() + timedelta(days=1)),
    #     "landing_datetime": str(datetime.now() + timedelta(days=1, hours=12)),
    #     "delayed_landing_time": ""
    # }

    # new_flight = Flight(
    #     aircraft_id=1022, 
    #     source="Tel Aviv", 
    #     destination="New York",
    #     departure_datetime=datetime.now() + timedelta(days=1),
    #     landing_datetime=datetime.now() + timedelta(days=1, hours=12),
    #     delayed_landing_time=""
    # )   
    
    #created_flight = flight_dal.create_flight(new_flight)
    # logger.info(f"Created flight id: {created_flight.id}, created flight des: {created_flight.destination}")

    # flight = flight_dal.get_flight(created_flight['id'])
    # logger.info(f"Retrieved flight: {flight}")

    # flight_dal.update_flight(created_flight['id'], {"arrival": "Los Angeles"})
    # updated_flight = flight_dal.get_flight(created_flight['id'])
    # logger.info(f"Updated flight: {updated_flight}")

    # flight_dal.delete_flight(created_flight['id'])
    # logger.info("Flight deleted")

    # flights = flight_dal.get_BGR_lands_next_5_hours()
    # #print each flight
    # for flight in flights:
    #     logger.info(f"Retrieved flight: {flight.destination}")  

    flights = flight_dal.get_flights_of_user("322361373")
    #print each flight
    for flight in flights:
        logger.info(f"Retrieved flight: {flight.id}")

def test_aircraft_dal(dal):
    logger.info("Testing AircraftDAL")
    aircraft_dal = dal.Aircraft

    # Assuming these methods exist. Adjust as necessary.
    # new_aircraft = {
    #     "manufacturer": "Boeing",
    #     "nickname": "Jumbo Jet",
    #     "YearOfManufacture": 1998,
    #     "ImageUrl": "https://picsum.photos/400/300",
    #     "NumberOfChairs": 400
    # }

    #declare a new aircraft object
    new_aircraft = Aircraft(
        manufacturer= "Boeing",
        nickname= "Jumbo Jet",
        year_of_manufacture= 1998,
        image_url= "https://picsum.photos/400/300",
        number_of_chairs= 400
    )   

    aircraft_dal.create_aircraft(new_aircraft)

    # logger.info(f"Created aircraft")

    #aircraft = aircraft_dal.get_aircraft(1023)
    #logger.info(f"Retrieved aircraft: {aircraft}")

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
        user_id= "322361373",
        purchase_datetime= datetime.now()
    )
    # created_ticket = ticket_dal.create_ticket(new_ticket)
    # logger.info(f"Created ticket: {created_ticket}")

    # ticket = ticket_dal.get_ticket(created_ticket['id'])
    # logger.info(f"Retrieved ticket: {ticket}")

    # ticket_dal.update_ticket(created_ticket['id'], {"seat_number": "14B"})
    # updated_ticket = ticket_dal.get_ticket(created_ticket['id'])
    # logger.info(f"Updated ticket: {updated_ticket}")

    # ticket_dal.delete_ticket(created_ticket['id'])
    # logger.info("Ticket deleted")

    # tickets = ticket_dal.get_tickets()
    # #print each ticket
    # for ticket in tickets:
    #     logger.info(f"Retrieved ticket: {ticket.id}")

    #check delete ticket
    ticket_dal.delete_ticket("193063")


def test_image_recognition_functionality(self):
        # Test get_image_tags
        aircraft_image_url = "https://d3m9l0v76dty0.cloudfront.net/system/photos/3169485/large/97e1a7cf208829e35c47b0dac9cfeb9c.jpg"
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

        url = "http://localhost:5001/api/image/analyze"

#test prediction dal
def test_prediction_dal(dal):

    flight_details = {
    "Season": "Winter",
    "FlightDistance": 1200,
    "FlightDuration": 90,
    "DepartureAirportCongestion": 30,
    "ArrivalAirportCongestion": 40,
    "DayOfWeek": "Monday",
    "TimeOfFlight": "08:00",
    "ScheduledDepartureTime": "07:30",
    "ActualDepartureTime": "07:45",
    "DepartureDelay": 15,
    "Temperature": 18.5,
    "Visibility": 10.0,
    "WindSpeed": 12.3,
    "WeatherEvent": "Clear"
    }

    is_delay= dal.Flight.is_landing_delayed(flight_details)
    if is_delay:
        print("Flight Delay Prediction: Yes")
    if not is_delay:
        print("Flight Delay Prediction: No")
    logger.info(f"Is flight delayed? {is_delay}")

#     app_server_url = "http://localhost:5001/api/prediction"
# # Convert the flight details into a JSON payload
#     headers = {'Content-Type': 'application/json'}
#     payload = json.dumps(flight_details)

# # Make a POST request to the app server
#     try:
#         response = requests.post(app_server_url, data=payload, headers=headers)

#     # Check the response status
#         if response.status_code == 200:
#         # Assuming the response is a simple boolean, print the result
#             is_delayed = response.json()
#             print("Flight Delay Prediction:", "Yes" if is_delayed else "No")
#         else:
#             print(f"Error: Received status code {response.status_code} - {response.text}")

#     except requests.exceptions.RequestException as e:
#         print(f"Error occurred while contacting the app server: {e}")






def main():

    api_client = APIClient()
    dal = DALFactory.get_instance()
    #test_image_recognition_functionality(dal)
    #dal = DALImpl()

    #test_date_checker(dal)
    #test_user_dal(dal)
    #test_flight_dal(dal)
    #test_aircraft_dal(dal)
    test_ticket_dal(dal)
    #test_prediction_dal(dal)



if __name__ == "__main__":
    main()
