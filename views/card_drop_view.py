import discord
from abstract_card_view import AbstractCardView
from drops.card_drop_event import CardDropEvent
from drops.card_drop_manager import CardDropManager

from views.card_drop_button_view import CardDropButtonView

class CardDropView(discord.ui.View):
    def __init__(self, drop_event: CardDropEvent):
        super().__init__(timeout=drop_event.DURATION_SECONDS)
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
        card_drop_manager = CardDropManager()
        card_drop_manager.on_event_timed_out(self.drop_event.id)
        return await super().on_timeout()


        
    
