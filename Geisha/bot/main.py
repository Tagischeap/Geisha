import asyncio
import threading
from config.logging_config import setup_logging
from config.env import load_and_validate_env_vars
from core.command_loader import load_commands
from commands.dalle import process_queue  # Import process_queue directly
from web.server import start_server

logger = setup_logging()
env_vars = load_and_validate_env_vars()

DISCORD_TOKEN = env_vars['DISCORD_TOKEN2']
PREFIX = env_vars['PREFIX']

import discord
from config.reload_manager import start_observer
from events.on_message import on_message as handle_on_message
from events.on_ready import on_ready as handle_on_ready

# Start the Flask server in a separate thread
flask_thread = threading.Thread(target=start_server)
flask_thread.daemon = True
flask_thread.start()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

logger.info("Starting the bot...")
load_commands()  # Populate the global COMMANDS dictionary

# Start the observer for reloading
observer = start_observer(client)

@client.event
async def on_ready():
    await handle_on_ready(client)
    logger.info("Bot is ready and connected.")
    
    if not hasattr(client, 'task_queue'):
        client.task_queue = asyncio.Queue()
        client.loop.create_task(process_queue(client))
        print("Queue processing started in on_ready.")

@client.event
async def on_message(message):
    await handle_on_message(client, message)

if __name__ == "__main__":
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to connect to Discord: {e}")
