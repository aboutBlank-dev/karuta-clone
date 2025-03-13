import discord

from database.models.user_card_model import UserCardModel
from discord_views.card_drop_view import CardDropButtonView
from drops.card_drop_event import CardDropEvent
from schemas.pokemon_card_schema import PokemonTCGCardLoader
from schemas.pokemon_card_set_schema import PokemonCardSetLoader
from user_manager import UserManager
from utils.id_utils import to_base36


class UserInventoryView(discord.ui.View):
    PREVIOUS_EMOJI ='️⬅️' 
    NEXT_EMOJI = '➡️'

    def __init__(self, discord_channel, discord_user_id: int):
        super().__init__(timeout=None)

        self.discord_channel = discord_channel
        self.discord_user_id = discord_user_id

        previous_button = InventoryPageNavigationButton(self.PREVIOUS_EMOJI)
        next_button = InventoryPageNavigationButton(self.NEXT_EMOJI)
        self.add_item(previous_button)
        self.add_item(next_button)

    async def start(self):
        all_cards = await UserManager.get_all_user_cards(self.discord_user_id)
        formatted_text = ""
        for i, card in enumerate(all_cards):
            tcg_card = PokemonTCGCardLoader.load_id(card.pokemon_tcg_card_id)
            tcg_set = PokemonCardSetLoader.load_id(tcg_card.set)

            formatted_text += f"`{to_base36(card.id)}`: {tcg_card.name} from **{tcg_set.name}**\n"

        embed = discord.Embed(title="🎴 Here is your Inventory!", description=f"Use the buttons to navigate to the next/previous pages. \n\n {formatted_text}", color=discord.Color.yellow())

        self.discord_inventory_message = await self.discord_channel.send(embed=embed, view=self)


class InventoryPageNavigationButton(discord.ui.Button):
    def __init__(self, emoji, *args, **kwargs):
        super().__init__(label=emoji, style=discord.ButtonStyle.grey, *args, **kwargs)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"GOO GOO GAH GAH TEST")