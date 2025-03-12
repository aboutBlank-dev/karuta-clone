import discord

from drops.card_drop_event import CardDropEvent


REACTION_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

class CardDropButtonView(discord.ui.Button):
    def __init__(self, card_index: int, drop_event: CardDropEvent, *args, **kwargs):
        # Initialize the button with the card's custom_id and other required arguments
        emoji = REACTION_EMOJIS[card_index]  # Assuming REACTION_EMOJIS is predefined
        custom_id = f"card_{card_index + 1}"

        super().__init__(emoji=emoji, style=discord.ButtonStyle.grey, custom_id=custom_id, *args, **kwargs)
        
        self.card_index = card_index
        self.drop_event = drop_event

    async def callback(self, interaction: discord.Interaction):
        """Handle the button click and process the card claim."""

        can_interact, error_message = self.drop_event.can_user_claim_card(interaction.user.id, self.card_index)

        if not can_interact:
            await interaction.response.send_message(f"{interaction.user.mention} {error_message}", ephemeral=True)
            return

        # Successful claim Send response to the user
        claimed_card = self.drop_event.claim_card_index(interaction.user.id, self.card_index)
        await interaction.response.send_message(f"{interaction.user.mention} claimed **{claimed_card.name}** from Drop `{self.drop_event.id}`!")

        # Update the view so that the button shows as disabled
        self.disabled = True
        await self.view.discord_drop_message.edit(view=self.view)

