import discord
from discord_views.card_drop_button_view import CardDropButtonView
from drops.card_drop_event import CardDropEvent

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