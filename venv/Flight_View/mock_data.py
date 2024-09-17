from datetime import datetime
from models.aircraft import Aircraft
from models.flight import Flight
from models.user import User
from models.ticket import Ticket

# Mock aircrafts data
aircrafts = [
    Aircraft(id=1, manufacturer='Boeing', nickname='SkyKing', year_of_manufacture=2010, image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDYCs6gNkh3kzGGdSfF5ew9eB72d_Qt5LIUA&s', number_of_chairs=300),
    Aircraft(id=2, manufacturer='Airbus', nickname='CloudMaster', year_of_manufacture=2015, image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDYCs6gNkh3kzGGdSfF5ew9eB72d_Qt5LIUA&s', number_of_chairs=250),
]

from datetime import datetime, timedelta

# Mock flights data
flights = [
    # Landing in 1 hour
    Flight(id=1, aircraft_id=1, source='New York', destination='Ben Gurion Airport',
           departure_datetime=datetime(2024, 9, 17, 6, 30), landing_datetime=datetime.now() + timedelta(hours=1)),

    # Landing in 2 hours
    Flight(id=2, aircraft_id=2, source='London', destination='Ben Gurion Airport',
           departure_datetime=datetime(2024, 9, 17, 7, 0), landing_datetime=datetime.now() + timedelta(hours=2)),

    # Landing in 3 hours
    Flight(id=3, aircraft_id=1, source='Paris', destination='Ben Gurion Airport',
           departure_datetime=datetime(2024, 9, 17, 8, 0), landing_datetime=datetime.now() + timedelta(hours=3)),

    # Landing in 4 hours
    Flight(id=4, aircraft_id=2, source='Berlin', destination='Ben Gurion Airport',
           departure_datetime=datetime(2024, 9, 17, 9, 0), landing_datetime=datetime.now() + timedelta(hours=4)),

    # Landing in 5 hours
    Flight(id=5, aircraft_id=1, source='Los Angeles', destination='Ben Gurion Airport',
           departure_datetime=datetime(2024, 9, 17, 5, 0), landing_datetime=datetime.now() + timedelta(hours=5)),

    # Flight that lands outside the 5-hour window for testing
    Flight(id=6, aircraft_id=1, source='Berlin', destination='Ben Gurion Airport',
           departure_datetime=datetime(2024, 9, 17, 1, 0), landing_datetime=datetime.now() + timedelta(hours=7)),

    # Flight that lands outside Ben Gurion for testing (won't show up)
    Flight(id=7, aircraft_id=2, source='Berlin', destination='Rome', departure_datetime=datetime(2024, 9, 17, 3, 0), landing_datetime=datetime.now() + timedelta(hours=2)),
    Flight(id=3, aircraft_id=1, source='Paris', destination='Berlin', departure_datetime=datetime(2024, 9, 17, 9, 0), landing_datetime=datetime(2024, 9, 17, 12, 0)),
    Flight(id=4, aircraft_id=2, source='Berlin', destination='Rome', departure_datetime=datetime(2024, 9, 18, 11, 0), landing_datetime=datetime(2024, 9, 18, 14, 0))
]


# Mock users data (including password field)
users = [
    User(id=1000, username='Dan', role='admin', first_name='Dan', last_name='Cohen', email='dan@gmail.com', password='2345'),
    User(id=1001, username='Tamar', role='passenger', first_name='Tamar', last_name='Hayat', email='tamar@gmail.com', password='1234')
]

# Mock tickets
tickets = [
    Ticket(id=1, flight_id=1, user_id=1001, purchase_datetime=datetime(2024, 9, 10, 12, 0)),
    Ticket(id=2, flight_id=2, user_id=1001, purchase_datetime=datetime(2024, 9, 11, 14, 0)),
    Ticket(id=3, flight_id=3, user_id=1000, purchase_datetime=datetime(2024, 9, 12, 10, 0)),
    Ticket(id=4, flight_id=4, user_id=1000, purchase_datetime=datetime(2024, 9, 13, 16, 0)),
    Ticket(id=5, flight_id=1, user_id=1001, purchase_datetime= datetime(2024,9,17, 8 , 50)) #2024-09-17 08:50)
]
