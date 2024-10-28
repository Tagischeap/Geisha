# main.py

import discord
import os
import logging
from colorama import init, Fore
from dotenv import load_dotenv
from events.on_message import handle_command
from events.on_message_react import react_to_message
from config.logging_config import setup_logging
from config.reload_manager import start_observer

import events.on_message
import events.on_message_react



# Load environment variables
load_dotenv(dotenv_path='keys.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN2')

version = "24.10.27"  # Replace with the actual version if needed

# Initialize colorama
init()

# Set up logging
logger = setup_logging()

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Start the Watchdog observer, passing the client
observer = start_observer(client)

# Event: on_ready
@client.event
async def on_ready():
    await display_bot_ready_info()

# Event: on_message
@client.event
async def on_message(message):
    """Handles incoming messages and delegates command processing."""
    if message.author == client.user:
        return
    logger.info(f"Message received: {message.content}")
    await handle_command(client, message)
    await react_to_message(client, message)
    
    # Use updated function references
    await events.on_message.handle_command(client, message)
    await events.on_message_react.react_to_message(client, message)

# Event: on_disconnect
@client.event
async def on_disconnect():
    observer.stop()  # Stop observer on bot shutdown

async def display_bot_ready_info():
    logger.info('----------------------------------------------------------------')
    logger.info(Fore.YELLOW + f'Logged in as ' + Fore.GREEN + f'{client.user.name}' + Fore.YELLOW + f' (ID: ' + Fore.CYAN + f'{client.user.id}' + Fore.YELLOW + f')')
    logger.info(f'Bot is connected to the following guilds:')
    for guild in client.guilds:
        logger.info(f' - ' + Fore.CYAN + f'{guild.name}' + Fore.WHITE + f' (ID: ' + Fore.CYAN + f'{guild.id}' + Fore.WHITE + f', Members: {guild.member_count})')

    logger.info('----------------------------------------------------------------')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'you. ({version})'))


# Run the bot
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)  # Start the bot with the Discord token
else:
    logger.error("Discord token not found. Please check your .env file.")
