class Aircraft:
    def __init__(self, id, manufacturer, nickname, year_of_manufacture, image_url, number_of_chairs):
        self.id = id
        self.manufacturer = manufacturer
        self.nickname = nickname
        self.year_of_manufacture = year_of_manufacture
        self.image_url = image_url
        self.number_of_chairs = number_of_chairs

    def __repr__(self):
        return f"<Aircraft(id={self.id}, manufacturer={self.manufacturer}, nickname={self.nickname}, year_of_manufacture={self.year_of_manufacture})>"

    def __str__(self):
        return f"Aircraft {self.id} - {self.manufacturer} ({self.year_of_manufacture}), Nickname: {self.nickname}"
