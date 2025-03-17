import discord

from database.models.user_card_model import UserCardModel
from pokemon_tcg_loader import PokemonTCGLoader
from utils.id_utils import to_base36

# TODO: Change this to use AbstractCardView instead
class CardView(discord.ui.View):
    def __init__(self, card: UserCardModel, discord_channel):
        super().__init__(timeout=None)

        self.card = card
        self.discord_channel = discord_channel

        self.tcg_card = PokemonTCGLoader.load_card_data(card.pokemon_tcg_card_id)
        self.tcg_set = PokemonTCGLoader.load_set_data(self.tcg_card.set)

        self.card_image = self.tcg_card.get_view().get_pattern_image_as_bytes(card.pattern_number, card.float_value)

    async def start(self):
        embed = discord.Embed(title=self.tcg_card.name, color=discord.Color.green())

        formatted_text = ""
        formatted_text += f"**Set**: `{self.tcg_set.name}`\n"
        formatted_text += f"**Float Value**: `{self.card.float_value}`\n"
        formatted_text += f"**Pattern Number**: `{self.card.pattern_number}`\n"

        embed.description = formatted_text;

        file_name = f"drop_{to_base36(self.card.id)}.png"
        file = discord.File(self.card_image, file_name)
        embed.set_image(url=f"attachment://{file_name}")

        self.discord_inventory_message = await self.discord_channel.send(embed=embed, file=file, view=self)