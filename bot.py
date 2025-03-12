import os
from dotenv import load_dotenv
import discord
import logging
from drops.card_drop_manager import CardDropManager
from card_display.pokemon_card_display import PokemonCardDisplay
from card_display.image_generator import create_drop_image
from discord.ext import commands

from schemas.pokemon_schema import PokemonSchema
from schemas.pokemon_card_schema import PokemonCardSchema, PokemonTCGCardLoader
from card_display.pokemon_tcg_card_display import PokemonTCGCardDisplay

# Load environment variables
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

# This example requires the 'message_content' intent.
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)
card_drop_manager = CardDropManager()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!drop':
        drop_event = card_drop_manager.create_drop_event_random(3, message)
        await drop_event.start()


# Log Handler
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log_handler.setLevel(logging.INFO)

client.run(discord_token, log_handler=log_handler)
