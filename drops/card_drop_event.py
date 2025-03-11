import uuid
from datetime import datetime

import pytz

from image_generator import create_drop_image
from pokemon_tcg_card import PokemonTCGCard

class CardDropEvent:
    DURATION_SECONDS = 60
    OWNER_ONLY_DURATION_SECONDS = 5

    """
    Represents a single drop event.
    """
    def __init__(self, cards: list[PokemonTCGCard], discord_message):
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
    
    def claim_card_index(self, user_id: int, card_index: int):
        self.claimed_cards[card_index] = user_id
        claimed_card = self.all_cards[card_index]
        return claimed_card
    
    def can_user_claim_card(self, user_id: int, card_index: int) -> tuple[bool, str]:
        if self.claimed_cards[card_index] is not None:
            return False, "This card has already been claimed."

        # Check if user has already claimed a card
        if user_id in self.claimed_cards:
            return False, "You have already claimed a card from this drop."

        # Owner can always interact (provided they haven't claimed one already)
        if user_id == self.owner_discord_id:
            return True, None
        
        # Check if Non-Owner time brace has expired
        timezone = pytz.timezone('UTC')  # Use UTC for consistency
        current_time = datetime.now(timezone)
        time_difference = current_time - self.created_at
        owner_only = time_difference.total_seconds() <= self.OWNER_ONLY_DURATION_SECONDS
        if owner_only:
            return False, f"You must wait at least {self.OWNER_ONLY_DURATION_SECONDS} seconds to claim someone else's drop. Time left: {time_difference.total_seconds()} seconds"
        else:
            return True, None
 
    def _get_discord_view(self):
        from views.card_drop_view import CardDropView
        return CardDropView(self)
        
    def _create_drop_image(self):
        all_card_views = [card.get_view() for card in self.all_cards]
        return create_drop_image(all_card_views)
