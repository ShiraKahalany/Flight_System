from dal.interfaces.idal import IImageRecognitionDAL
from typing import List
from exceptions import ImageAnalysisException, NetworkException, UnexpectedErrorException
import requests

class ImageRecognitionDAL(IImageRecognitionDAL):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_image_tags(self, image_url: str) -> List[str]:
        try:
            response = self.api_client.get("image/analyze", params={"imageUrl": image_url})
            #response = requests.get(f"image/analyze/{image_url}")
            return response.text
        except requests.exceptions.HTTPError as e:
            raise ImageAnalysisException(f"Error analyzing image: {e}") from e
        except NetworkException as e:
            raise NetworkException(f"Network error during image analysis: {e}") from e
        except Exception as e:
            raise UnexpectedErrorException(f"Unexpected error during image analysis: {e}") from e

    def is_aircraft_image(self, image_url: str) -> bool:
        desc = self.get_image_tags(image_url)
        aircraft_related_tags = {'airplane', 'aircraft', 'plane', 'jet'}
        tags = desc.split('\n')
        return any(tag.lower() in aircraft_related_tags for tag in tags)