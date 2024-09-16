from dal.interfaces.idal import IImageRecognitionDAL
from typing import List

class ImageRecognitionDAL(IImageRecognitionDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_image_tags(self, image_url: str) -> List[str]:
        
        print(f"Sending request to: {self.api_client.base_url}/image/analyze")
        print(f"With data: {{'imageUrl': {image_url}}}")

        response = self.api_client.post("image/analyze", data={"imageUrl": image_url})
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        return response.get('tags', [])
        


    def is_aircraft_image(self, image_url: str) -> bool:
        tags = self.get_image_tags(image_url)
        aircraft_related_tags = {'airplane', 'aircraft', 'plane', 'jet'}
        return any(tag.lower() in aircraft_related_tags for tag in tags)