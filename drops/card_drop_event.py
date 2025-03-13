import uuid
from datetime import datetime
import pytz
from card_display.image_generator import create_drop_image
from schemas.pokemon_card_schema import PokemonCardSchema

class CardDropEvent:
    DURATION_SECONDS = 60
    OWNER_ONLY_DURATION_SECONDS = 5

    """
    Represents a single drop event.
    """
    def __init__(self, cards: list[PokemonCardSchema], discord_message):
        self.id = str(uuid.uuid4())
        self.owner_discord_id = discord_message.author.id
        self.discord_channel = discord_message.channel
        self.created_at = discord_message.created_at
        self.all_cards = cards

        self.drop_image = self._create_drop_image()
        self.claimed_cards = [None for _ in range(len(self.all_cards))]
    
    async def start(self):
        view = self._get_discord_view()
        return await view.start()
    
    def _get_discord_view(self):
        from discord_views.card_drop_view import CardDropView
        return CardDropView(self)
        
    def _create_drop_image(self):
        all_card_views = [card.get_view() for card in self.all_cards]
        return create_drop_image(all_card_views)
