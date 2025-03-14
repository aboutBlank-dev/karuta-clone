from abc import ABC, abstractmethod
import io

class AbstractCardDisplay(ABC):
    CARD_WIDTH: int
    CARD_HEIGHT: int

    @abstractmethod
    def create_image(self):
        pass

    @abstractmethod
    def create_pattern_image(self, pattern_number, float_value):
        pass
    
    @abstractmethod
    def get_display_name(self):
        pass

    def get_image_as_bytes(self):
        image = self.create_image()
        return self._get_as_bytes(image)
    
    def get_pattern_image_as_bytes(self, pattern_number, float_value):
        image = self.create_pattern_image(pattern_number, float_value)
        return self._get_as_bytes(image)

    def _get_as_bytes(self, image):
        byte_io = io.BytesIO()
        image.save(byte_io, 'PNG')  # Save as PNG with transparency
        byte_io.seek(0)

        return byte_io