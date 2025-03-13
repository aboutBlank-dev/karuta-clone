import os
from dotenv import load_dotenv
import discord
import logging
from drops.card_drop_event_handler import CardDropEventHandler

from user_manager import UserManager

# Load environment variables
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

# This example requires the 'message_content' intent.
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!drop':
        await UserManager.get_or_create(message.author.id)
        drop_event = await CardDropEventHandler.create_drop_event_random(3, message)
        await drop_event.start()
    
    if message.content == "!inv":
        all_user_cards = await UserManager.get_all_user_cards(message.author.id)

        card_ids = "\n".join(str(card.pokemon_tcg_card_id) for card in all_user_cards)
        # Send the message with all the card ids
        await message.channel.send(f"Your cards:\n{card_ids}")


# Log Handler
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log_handler.setLevel(logging.INFO)

client.run(discord_token, log_handler=log_handler)
