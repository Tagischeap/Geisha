import discord
import os
import logging
from colorama import init, Fore
from dotenv import load_dotenv
from config.logging_config import setup_logging
from config.reload_manager import start_observer
from core.command_handler import load_commands
from events.on_message import on_message as handle_on_message
from events.on_message_react import react_to_message
from events.on_ready import on_ready as handle_on_ready

# Load environment variables
load_dotenv(dotenv_path='keys.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Set up logging
logger = setup_logging()

# Initialize Discord client with specific intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Load commands only once here
load_commands()

# Start the Watchdog observer for file reloads
observer = start_observer(client)

# Event listeners
@client.event
async def on_ready():
    await handle_on_ready(client)  # Use the on_ready from events module

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await handle_on_message(client, message)
    await react_to_message(client, message)

@client.event
async def on_disconnect():
    observer.stop()

# Run the bot
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)
else:
    logger.error("Discord token not found. Please check your .env file.")
