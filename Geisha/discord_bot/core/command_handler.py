# core/command_handler.py
import importlib
import os
import logging
import discord

logger = logging.getLogger(__name__)

COMMANDS = {}

async def handle_command(client, message: discord.Message, command_name: str, args: list):
    """
    Executes a command if found in the COMMANDS dictionary, considering aliases.
    """
    # Check for the command by name or alias
    command = COMMANDS.get(command_name) or next(
        (cmd for cmd in COMMANDS.values() if command_name in cmd['aliases']), None
    )

    if command:
        try:
            await command['execute'](client, message, args)
            logger.info(f"Executed command '{command_name}' with args: {args}")
        except Exception as e:
            logger.error(f"Error executing command '{command_name}': {e}")
            await message.channel.send(f"An error occurred while executing `{command_name}`.")
    else:
        # Friendly message if command or alias is unknown
        logger.warning(f"Unknown command: '{command_name}' from {message.author}")
        await message.channel.send(
            f"Unknown command: `{command_name}`. Type `{os.getenv('PREFIX', '!')}help` to see available commands."
        )
