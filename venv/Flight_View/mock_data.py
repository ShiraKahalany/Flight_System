from datetime import datetime

# Mock aircrafts data
aircrafts = [
    {'id': 1, 'manufacturer': 'Boeing', 'nickname': 'SkyKing', 'year_of_manufacture': 2010, 'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDYCs6gNkh3kzGGdSfF5ew9eB72d_Qt5LIUA&s'},
    {'id': 2, 'manufacturer': 'Airbus', 'nickname': 'CloudMaster', 'year_of_manufacture': 2015, 'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDYCs6gNkh3kzGGdSfF5ew9eB72d_Qt5LIUA&s'}
]

# Mock flights data
flights = [
    {'id': 1, 'aircraft_id': 1, 'source': 'New York', 'destination': 'Ben Gurion Airport', 'departure_datetime': datetime(2024, 9, 15, 10, 30), 'landing_datetime': datetime(2024, 9, 15, 18, 30)},
    {'id': 2, 'aircraft_id': 2, 'source': 'London', 'destination': 'Ben Gurion Airport', 'departure_datetime': datetime(2024, 9, 16, 14, 30), 'landing_datetime': datetime(2024, 9, 16, 21, 30)},
    {'id': 3, 'aircraft_id': 1, 'source': 'Paris', 'destination': 'Berlin', 'departure_datetime': datetime(2024, 9, 17, 9, 0), 'landing_datetime': datetime(2024, 9, 17, 12, 0)},
    {'id': 4, 'aircraft_id': 2, 'source': 'Berlin', 'destination': 'Rome', 'departure_datetime': datetime(2024, 9, 18, 11, 0), 'landing_datetime': datetime(2024, 9, 18, 14, 30)},
    {'id': 5, 'aircraft_id': 1, 'source': 'Los Angeles', 'destination': 'Ben Gurion Airport', 'departure_datetime': datetime(2024, 9, 19, 8, 0), 'landing_datetime': datetime(2024, 9, 19, 16, 0)}
]

# Mock users
users = [
    {'id': 1000, 'username': 'Dan', 'password_hash': '2345', 'role': 'admin', 'first_name': 'Dan', 'last_name': 'Cohen', 'email': 'dan@gmail.com'},
    {'id': 1001, 'username': 'Tamar', 'password_hash': '1234', 'role': 'passenger', 'first_name': 'Tamar', 'last_name': 'Hayat', 'email': 'tamar@gmail.com'}
]

# Mock tickets
tickets = [
    {'id': 1, 'flight_id': 1, 'user_id': 1001, 'purchase_datetime': datetime(2024, 9, 10, 12, 0)},
    {'id': 2, 'flight_id': 2, 'user_id': 1001, 'purchase_datetime': datetime(2024, 9, 11, 14, 0)},
    {'id': 3, 'flight_id': 3, 'user_id': 1000, 'purchase_datetime': datetime(2024, 9, 12, 10, 0)},
    {'id': 4, 'flight_id': 4, 'user_id': 1000, 'purchase_datetime': datetime(2024, 9, 13, 16, 0)}
]
