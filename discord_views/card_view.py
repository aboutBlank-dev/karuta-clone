import discord

from database.models.user_card_model import UserCardModel
from schemas.pokemon_card_schema import PokemonTCGCardLoader
from schemas.pokemon_card_set_schema import PokemonCardSetLoader
from utils.id_utils import to_base36

# TODO: Change this to use AbstractCardView instead
class CardView(discord.ui.View):
    def __init__(self, card: UserCardModel, discord_channel):
        super().__init__(timeout=None)

        self.card = card
        self.discord_channel = discord_channel

        self.tcg_card = PokemonTCGCardLoader.load_id(card.pokemon_tcg_card_id)
        self.tcg_set = PokemonCardSetLoader.load_id(self.tcg_card.set)

        self.card_image = self.tcg_card.get_view().get_pattern_image_as_bytes(card.pattern_number, card.float_value)

    async def start(self):
        embed = discord.Embed(title=self.tcg_card.name, description=self.tcg_set.name, color=discord.Color.green())

        file_name = f"drop_{to_base36(self.card.id)}.png"
        file = discord.File(self.card_image, file_name)
        embed.set_image(url=f"attachment://{file_name}")

        self.discord_inventory_message = await self.discord_channel.send(embed=embed, file=file, view=self)