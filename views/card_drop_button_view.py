import discord


REACTION_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

class CardDropButtonView(discord.ui.Button):
    def __init__(self, card_index: int, *args, **kwargs):
        # Initialize the button with the card's custom_id and other required arguments
        emoji = REACTION_EMOJIS[card_index]  # Assuming REACTION_EMOJIS is predefined
        custom_id = f"card_{card_index + 1}"

        super().__init__(emoji=emoji, style=discord.ButtonStyle.grey, custom_id=custom_id, *args, **kwargs)
        
        self.card_index = card_index

    async def callback(self, interaction: discord.Interaction):
        """Handle the button click and process the card claim."""
        from views.card_drop_view import CardDropView

        card_drop_view: CardDropView = self.view
        await card_drop_view.try_claim(interaction, self.card_index)
