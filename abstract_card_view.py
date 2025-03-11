from abc import ABC, abstractmethod

class AbstractCardView(ABC):
    CARD_WIDTH: int
    CARD_HEIGHT: int

    @abstractmethod
    def create_image(self):
        pass
    
    @abstractmethod
    def get_display_name(self):
        pass