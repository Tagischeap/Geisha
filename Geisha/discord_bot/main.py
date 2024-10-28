import discord
import os
import logging
from colorama import init, Fore, Style  # Style points
from dotenv import load_dotenv
from events.on_message import handle_command  # Import the command handler
from events.on_message_react import react_to_message  # Import the custom reaction handler

# Load environment variables
load_dotenv(dotenv_path='keys.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

version = "24.10.27"  # Replace with the actual version if needed

init()  # Initialize colorama
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
    logger.info(Fore.YELLOW + f'Logged in as ' + Fore.GREEN + f'{client.user.name}' + Fore.YELLOW + f' (ID: ' + Fore.CYAN + f'{client.user.id}' + Fore.YELLOW + f')')
    logger.info(f'Bot is connected to the following guilds:')
    for guild in client.guilds:
        logger.info(f' - ' + Fore.CYAN + f'{guild.name}' + Fore.WHITE + f' (ID: ' + Fore.CYAN + f'{guild.id}' + Fore.WHITE + f', Members: {guild.member_count})')
    logger.info('----------------------------------------------------------------')
    
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'you. ({version})'))

@client.event
async def on_message(message):
    """Handles incoming messages and delegates command processing."""
    logger.info(f"Message received: {message.content}")  # Log the received message content
    if message.author == client.user:  # Ignore messages from the bot itself
        logger.info("Message is from the bot itself; ignoring.")
        return  # Exit the function if the message is from the bot

    await handle_command(client, message)  # Call the command handler function
    await react_to_message(client, message)  # Call the custom reaction handler

# Run the bot
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)  # Start the bot with the Discord token
else:
    logger.error("Discord token not found. Please check your .env file.")
