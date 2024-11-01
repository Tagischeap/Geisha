# main.py

# Import and set up logging at the start
from config.logging_config import setup_logging
logger = setup_logging()

# Proceed with the rest of the imports and bot setup
import discord
import os
from dotenv import load_dotenv
from config.reload_manager import start_observer
from core.command_handler import load_commands
from events.on_message import on_message as handle_on_message
from events.on_message_react import react_to_message
from events.on_ready import on_ready as handle_on_ready

# Load environment variables
load_dotenv(dotenv_path='keys.env')

def validate_env_vars():
    """Validates essential environment variables and stops the bot if any are missing."""
    missing_vars = []
    required_vars = ['DISCORD_TOKEN', 'OPENAI_API_KEY', 'PREFIX']
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            logger.error(f"Environment variable {var} is missing.")
    
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}. Check your keys.env file.")

# Validate environment variables before proceeding
validate_env_vars()

# Retrieve essential environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '!')

# Initialize Discord client with specific intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Log bot startup
logger.info("Starting the bot...")

# Load commands only once here
load_commands()

# Start the Watchdog observer for file reloads
observer = start_observer(client)

# Event listeners
@client.event
async def on_ready():
    await handle_on_ready(client)
    logger.info("Bot is ready and connected.")

@client.event
async def on_message(message):
    await handle_on_message(client, message)

@client.event
async def on_reaction_add(reaction, user):
    await react_to_message(client, reaction.message)

# Run the bot within the main scope
if __name__ == "__main__":
    try:
        client.run(DISCORD_TOKEN)  # Attempt to run the bot
    except Exception as e:
        logger.error(f"Failed to connect to Discord: {e}")
