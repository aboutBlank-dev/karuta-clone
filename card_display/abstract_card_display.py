from abc import ABC, abstractmethod

class AbstractCardDisplay(ABC):
    CARD_WIDTH: int
    CARD_HEIGHT: int

    @abstractmethod
    def create_image(self):
        pass

    @abstractmethod
    def get_image_as_bytes(self):
        pass
    
    @abstractmethod
    def get_display_name(self):
        pass