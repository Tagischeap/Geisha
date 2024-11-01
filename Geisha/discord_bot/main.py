# main.py

from config.logging_config import setup_logging
from config.env import load_and_validate_env_vars
from core.command_loader import load_commands

logger = setup_logging()
env_vars = load_and_validate_env_vars()

DISCORD_TOKEN = env_vars['DISCORD_TOKEN']
PREFIX = env_vars['PREFIX']

import discord
from config.reload_manager import start_observer
from events.on_message import on_message as handle_on_message
from events.on_message_react import react_to_message
from events.on_ready import on_ready as handle_on_ready

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

logger.info("Starting the bot...")
commands = load_commands()
observer = start_observer(client)

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

if __name__ == "__main__":
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to connect to Discord: {e}")
