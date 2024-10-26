import discord
import os
import logging
from dotenv import load_dotenv
# Load environment variables
load_dotenv(dotenv_path='keys.env')  
from events.on_message import handler  # Ensure this line is correct

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')  # Clean format
logger = logging.getLogger(__name__)

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info('----------------------------------------------------------------')
    logger.info(f'Logged in as {client.user.name}!')
    logger.info(f'Application: {client.user.name}')
    logger.info('----------------------------------------------------------------')
   # Set bot activity to watching status
    version = "2410.25"  # Replace with the actual version if needed
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'you. ({version})'))

@client.event
async def on_message(message):
    await handler(client, message)  # This should now work if the handler is properly imported

# Run the bot
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)
else:
    logger.error("Discord token not found. Please check your .env file.")
