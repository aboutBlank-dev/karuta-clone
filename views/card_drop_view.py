import discord
from card import Card
from image_generator import create_drop_image
from pokemon import Pokemon
import uuid

from views.card_drop_button_view import CardDropButtonView

class CardDropView(discord.ui.View):
    def __init__(self, cards: list[Card], discord_user, discord_channel):
        super().__init__(timeout=None)

        self.drop_id = str(uuid.uuid4())

        self.cards = cards
        self.drop_image = create_drop_image(cards)
        self.claimed = False

        self.discord_user = discord_user
        self.discord_channel = discord_channel
        self.discord_drop_message = None

        for i, card in enumerate(self.cards):
            # Create a dynamic button for each card
            button = CardDropButtonView(card_index=i)
            self.add_item(button)

    async def start(self):
        embed = discord.Embed(title="🎴 Cards have appeared!", description="React to claim a card!", color=discord.Color.blue())
        
        file_name = f"drop_{self.drop_id}.png"
        file = discord.File(self.drop_image, file_name)
        embed.set_image(url=f"attachment://{file_name}")

        self.discord_drop_message = await self.discord_channel.send(embed=embed, file=file, view=self)
    
    async def try_claim(self, interaction, card_index):
        if self.claimed:
            return await interaction.response.send_message("This drop has already been claimed.", ephemeral=True)

        # Mark drop as claimed
        self.claimed = True

        claimed_card: Card = self.cards[card_index]
        
        # Send response to the user
        await interaction.response.send_message(f"{interaction.user.mention} claimed **{claimed_card.pokemon.get_formatted_name()}** from Drop `{self.drop_id}`!", ephemeral=True)
        
        # Edit message to remove buttons after claiming
        await self.discord_drop_message.edit(view=None)

    """Automatically called when user tries to interact with this View"""
    async def interaction_check(self, interaction):
        if self.claimed:
            return False

        return True


        
    
