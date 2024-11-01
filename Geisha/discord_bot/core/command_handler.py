# core/command_handler.py
import logging
import discord
from core.command_loader import COMMANDS  # Import COMMANDS directly

logger = logging.getLogger(__name__)

async def handle_command(client, message: discord.Message, command_name: str, args: list):
    """
    Executes a command if found in the COMMANDS dictionary, considering aliases.
    """
    command = COMMANDS.get(command_name) or next(
        (cmd for cmd in COMMANDS.values() if command_name in cmd['aliases']), None
    )

    if command:
        try:
            if command_name == "help":  # Special handling for help command
                await command['execute'](client, message, args, COMMANDS)
            else:
                await command['execute'](client, message, args)
            logger.info(f"Executed command '{command_name}' with args: {args}")
        except Exception as e:
            logger.error(f"Error executing command '{command_name}': {e}")
            await message.channel.send(f"An error occurred while executing `{command_name}`.")