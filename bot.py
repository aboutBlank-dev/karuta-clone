import os
from dotenv import load_dotenv
import discord
import logging
from card import Card
from image_generator import create_image
import random

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

# List of possible colors and titles for randomness
colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
titles = ['Tiago', 'Onur', 'Jose', 'Mondim', 'Pere']

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!create_image':
        cards = [Card(random.choice(titles), random.choice(colors)) for _ in range(3)]
        image = create_image(cards)
        await message.channel.send(file=discord.File(fp=image, filename='image.png'))


# Log Handler
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log_handler.setLevel(logging.INFO)

client.run(discord_token, log_handler=log_handler)
