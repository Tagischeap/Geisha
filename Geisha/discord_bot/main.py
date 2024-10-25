import discord
import os
import logging
from dotenv import load_dotenv
from events.on_message import handler
from config.logging_config import setup_logging

# Load environment variables
load_dotenv(dotenv_path='keys.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'Bot is ready and connected as {client.user}!')

@client.event
async def on_message(message):
    await handler(client, message)

# Run the bot
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)
else:
    logger.error("Discord token not found. Please check your .env file.")
