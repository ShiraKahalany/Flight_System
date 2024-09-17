from dal.interfaces.idal import IImageRecognitionDAL
from typing import List

class ImageRecognitionDAL(IImageRecognitionDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_image_tags(self, image_url: str) -> List[str]:
        response = self.api_client.post("image/analyze", data={"imageUrl": image_url})
        return response.text
        


    def is_aircraft_image(self, image_url: str) -> bool:
        desc = self.get_image_tags(image_url)
        aircraft_related_tags = {'airplane', 'aircraft', 'plane', 'jet'}
        tags = desc.split('\n')
        return any(tag.lower() in aircraft_related_tags for tag in tags)