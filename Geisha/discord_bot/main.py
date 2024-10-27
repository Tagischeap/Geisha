import discord
import os
import logging
from dotenv import load_dotenv
from events.on_message import handle_command  # Import the command handler

# Load environment variables
load_dotenv(dotenv_path='keys.env')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')  # Clean format
logger = logging.getLogger(__name__)

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info('----------------------------------------------------------------')
    logger.info(f'Logged in as {client.user.name}!')
    logger.info(f'Application: {client.user.name}')
    logger.info('----------------------------------------------------------------')
    version = "2410.25"  # Replace with the actual version if needed
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'you. ({version})'))

@client.event
async def on_message(message):
    """Handles incoming messages and delegates command processing."""
    logger.info(f"Message received: {message.content}")  # Log the received message content
    if message.author == client.user:  # Ignore messages from her
        logger.info("Message is from the bot itself; ignoring.")
        return  # Exit the function if the message is from her

    await handle_command(client, message)  # Call the command handler function

# Run the bot
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)  # Start the bot with the Discord token
else:
    logger.error("Discord token not found. Please check your .env file.")
