import io
from card_display.abstract_card_display import AbstractCardDisplay

from schemas.pokemon_card_schema import PokemonCardSchema
from scripts.pokemon_tcg_saver import load_pokemon_tcg_card_image

class PokemonTCGCardDisplay(AbstractCardDisplay):
    CARD_WIDTH = 240
    CARD_HEIGHT = 330

    def __init__(self, card: PokemonCardSchema):
        self.card = card
    
    def create_image(self):
        image = load_pokemon_tcg_card_image(self.card.id)
        image = image.resize((self.CARD_WIDTH, self.CARD_HEIGHT))
        return image
    
    def get_image_as_bytes(self):
        image = self.create_image()
        byte_io = io.BytesIO()
        image.save(byte_io, 'PNG')  # Save as PNG with transparency
        byte_io.seek(0)

        return byte_io


    def get_display_name(self):
        return self.card.name

