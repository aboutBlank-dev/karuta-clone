import os
from dotenv import load_dotenv
import discord
import logging
from discord_views.card_view import CardView
from discord_views.user_inventory_view import UserInventoryView
from drops.card_drop_event_handler import CardDropEventHandler

from database.managers.user_manager import UserManager

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

    if message.content == "!help":
        help_message = ""
        help_message += "List of commands:\n"
        help_message += "`!drop` Drop Cards\n"
        help_message += "`!inv`  Check all your cards\n"
        help_message += "`!view <card_id>` View a card\n"
        await message.channel.send(help_message)
        return

    await UserManager.get_or_create(message.author.id)

    if message.content == '!drop':
        drop_event = await CardDropEventHandler.create_drop_event_random(3, message)
        await drop_event.start()
        return
    
    if message.content == "!inv":
        inventory_view = UserInventoryView(message.channel, message.author.id)
        await inventory_view.start()
        return

    if message.content.startswith("!view"):
        parts = message.content.split()
        
        if len(parts) == 2:
            card_id = parts[1]
            card = await UserManager.get_user_card(card_id)

            if card is None:
                await message.channel.send("Please double check the card ID.")
                return

            card_view = CardView(card, message.channel)
            await card_view.start()
        else:
            await message.channel.send("Please provide an ID after the !view command and nothing else")
        
        return



# Log Handler
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log_handler.setLevel(logging.INFO)

client.run(discord_token, log_handler=log_handler)
