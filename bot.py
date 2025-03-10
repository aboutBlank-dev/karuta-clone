import os
from dotenv import load_dotenv
import discord
import logging
from card import Card
from image_generator import create_image
import random

from pokemon import Pokemon

# Load environment variables
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

# This example requires the 'message_content' intent.
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!drop':
        cards = [Card(Pokemon(), 'white') for _ in range(3)]
        image = create_image(cards)
        await message.channel.send(f"{message.author.mention} Here are your drops:", file=discord.File(fp=image, filename='image.png'))

        for card in cards:
            if card.pokemon.is_shiny:
                await message.channel.send("Shiny Pokemon found!")
                break

# Log Handler
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log_handler.setLevel(logging.INFO)

client.run(discord_token, log_handler=log_handler)
