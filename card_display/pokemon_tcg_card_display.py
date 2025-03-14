from card_display.abstract_card_display import AbstractCardDisplay
from PIL import Image
from schemas.pokemon_card_schema import PokemonCardSchema
from scripts.image_generator import apply_pattern_damage, generate_seed
from scripts.pokemon_tcg_saver import load_pokemon_tcg_card_image

class PokemonTCGCardDisplay(AbstractCardDisplay):
    CARD_WIDTH = 240
    CARD_HEIGHT = 330

    def __init__(self, card: PokemonCardSchema):
        self.card = card
    
    def create_image(self):
        try:
            image = load_pokemon_tcg_card_image(self.card.id)
            image = image.resize((self.CARD_WIDTH, self.CARD_HEIGHT))
            return image
        except Exception as e:
            print(e)
            return Image.new("RGBA", (self.CARD_WIDTH, self.CARD_HEIGHT), (255, 255, 255))

    
    def create_pattern_image(self, pattern_number, float_value):
        image = self.create_image()

        seed = generate_seed(pattern_number=pattern_number, card_id=self.card.id)
        image = apply_pattern_damage(image, seed, float_value)
        return image

    def get_display_name(self):
        return self.card.name

