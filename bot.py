import os
from dotenv import load_dotenv
import discord
import logging
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

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #Log the message
    print(f'{message.author} said: {message.content}')



# Log Handler
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log_handler.setLevel(logging.INFO)

client.run(discord_token, log_handler=log_handler)
