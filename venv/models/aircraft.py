from typing import Optional
from pydantic import BaseModel, Field

import json

class Aircraft:
    def __init__(self, manufacturer, nickname, year_of_manufacture, image_url, number_of_chairs, id=None):
        #None if id not provided
        self.id: Optional[int]=id
        self.manufacturer = manufacturer
        self.nickname = nickname
        self.year_of_manufacture = year_of_manufacture
        self.image_url = image_url
        self.number_of_chairs = number_of_chairs

    def to_server_format(self):
        """Convert the object to JSON for sending to the server."""
        server_dict = {
            #'Id': int(self.id),
            'Manufacturer': str(self.manufacturer),
            'Nickname': str(self.nickname),
            'YearOfManufacture': int(self.year_of_manufacture),
            'ImageUrl': str(self.image_url),
            'NumberOfChairs': int(self.number_of_chairs)
        }
        return server_dict


    @classmethod
    def to_client_format(cls, server_dict):
        """Create an Aircraft object from DICT received from the server."""
        return cls(
            id=int(server_dict["id"]),
            manufacturer=server_dict["manufacturer"],
            nickname=server_dict["nickname"],
            year_of_manufacture=int(server_dict["yearOfManufacture"]),
            image_url=server_dict["imageUrl"],
            number_of_chairs=int(server_dict["numberOfChairs"])
        )
    
    def __repr__(self):
        return f"<Aircraft(id={self.id}, manufacturer={self.manufacturer}, nickname={self.nickname}, year_of_manufacture={self.year_of_manufacture})>"

    def __str__(self):
        return f"Aircraft {self.id} - {self.manufacturer} ({self.year_of_manufacture}), Nickname: {self.nickname}"
