import io
import uuid
from datetime import datetime
from schemas.pokemon_card_schema import PokemonCardSchema
from PIL import Image

class CardDropEvent:
    DURATION_SECONDS = 60
    OWNER_ONLY_DURATION_SECONDS = 5

    """
    Represents a single drop event.
    """
    def __init__(self, cards: list[PokemonCardSchema], discord_message):
        self.id = str(uuid.uuid4())
        self.discord_author = discord_message.author
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
        
    def _create_drop_image(self, spacing: int = 20, padding: int = 20):
        cards = [card.get_view() for card in self.all_cards]
        # Calculate combined width and height including spacing and padding
        # We generate first card ahead of time since we need to update the width/height (which we get from the loaded image)
        first_card = cards[0]
        first_card_image = first_card.create_image()

        combined_width = (first_card.CARD_WIDTH * len(cards)) + (spacing * (len(cards) - 1)) + (2 * padding)
        combined_height = first_card.CARD_HEIGHT + (2 * padding)

        # Create a new image with the specified width and height
        combined_image = Image.new("RGBA", (combined_width, combined_height), (0, 0, 0, 0))  # Transparent background

        # Place the cards on the combined image with spacing
        for i, card in enumerate(cards):
            card_image = first_card_image if (i == 0) else card.create_image()  
            alpha_channel = card_image.split()[3]  # Get the alpha channel (the 4th channel)

            # Calculate the position considering padding and spacing between cards
            x_position = padding + i * (card.CARD_WIDTH + spacing)
            y_position = padding

            # Paste the card image onto the combined image with its alpha channel as a mask
            combined_image.paste(card_image, (x_position, y_position), alpha_channel)

        # Save the image to a BytesIO object
        byte_io = io.BytesIO()
        combined_image.save(byte_io, 'PNG')  # Save as PNG with transparency
        byte_io.seek(0)

        return byte_io

