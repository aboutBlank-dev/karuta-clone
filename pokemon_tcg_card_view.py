
from abstract_card_view import AbstractCardView

from pokemon_tcg_card import PokemonTCGCard
from scripts.pokemon_tcg_saver import load_pokemon_tcg_card_image

class PokemonTCGCardView(AbstractCardView):
    CARD_WIDTH = 240
    CARD_HEIGHT = 330

    def __init__(self, card: PokemonTCGCard = None):
        self.card = card
    
    def create_image(self):
        image = load_pokemon_tcg_card_image(self.card.pokemon_tcg_card_data["id"])
        image.resize((self.CARD_WIDTH, self.CARD_HEIGHT))
        return image
    
    def get_display_name(self):
        return self.card.get_name()

