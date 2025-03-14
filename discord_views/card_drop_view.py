import discord
from drops.card_drop_event import CardDropEvent
from drops.card_drop_event import CardDropEvent
from drops.card_drop_event_handler import CardDropEventHandler

REACTION_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

class CardDropView(discord.ui.View):
    def __init__(self, drop_event: CardDropEvent):
        super().__init__(timeout=CardDropEvent.DURATION_SECONDS)
        self.drop_event = drop_event
        self.discord_channel = drop_event.discord_channel

        for i, card in enumerate(drop_event.all_cards):
            button = CardDropButtonView(card_index=i, drop_event=drop_event)
            self.add_item(button)

    async def start(self):
        embed = discord.Embed(title="🎴 Cards have appeared!", description="React to claim a card!", color=discord.Color.blue())
        
        file_name = f"drop_{self.drop_event.id}.png"
        file = discord.File(self.drop_event.drop_image, file_name)
        embed.set_image(url=f"attachment://{file_name}")

        self.discord_drop_message = await self.discord_channel.send(embed=embed, file=file, view=self)
    
    async def on_timeout(self):
        file_name = f"drop_{self.drop_event.id}.png"
        expired_embed = discord.Embed(title="🎴 Drop has expired !", color=discord.Color.light_grey())
        expired_embed.set_image(url=f"attachment://{file_name}")

        all_cards = self.drop_event.all_cards
        claimed_cards = self.drop_event.claimed_cards

        formatted_text = ""
        for i, card in enumerate(all_cards):
            if claimed_cards[i] is not None:
                formatted_text += f"✅ {card.name} was caught!\n"  # Checkmark for caught cards
            else:
                formatted_text += f"❌ {card.name} was lost forever!\n"  # Cross for lost cards

        expired_embed.set_footer(text=formatted_text)

        await self.discord_drop_message.edit(embed=expired_embed, view=None)
        return await super().on_timeout()


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

        can_interact, error_message = CardDropEventHandler.can_user_claim_card(self.drop_event, interaction.user.id, self.card_index)

        if not can_interact:
            await interaction.response.send_message(f"{interaction.user.mention} {error_message}", ephemeral=True)
            return

        try:
            claimed_card = await CardDropEventHandler.claim_card_index(self.drop_event, interaction.user.id, self.card_index)
            await interaction.response.send_message(f"{interaction.user.mention} claimed **{claimed_card.name}** from Drop `{self.drop_event.id}`!")
        except Exception as e:
            print(e)
            await interaction.response.send_message(f"There was an error claiming your card. Try again.", ephemeral=True)
            return;

        # Update the view so that the button shows as disabled
        self.disabled = True
        await self.view.discord_drop_message.edit(view=self.view)