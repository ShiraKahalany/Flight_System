from abc import ABC, abstractmethod
from typing import List


class IImageRecognitionDAL(ABC):
    # Image recognition-related abstract methods
    @abstractmethod
    def get_image_tags(self, image_url: str) -> List[str]:
        pass

    @abstractmethod
    def is_aircraft_image(self, image_url: str) -> bool:
        pass