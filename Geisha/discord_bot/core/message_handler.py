# core/message_handler.py
import discord
import logging
import os
from dotenv import load_dotenv
from core.command_handler import handle_command, COMMANDS

# Load environment variables from keys.env
load_dotenv()

# Retrieve the command prefix from environment variables, default to "!" if not specified
PREFIX = os.getenv('PREFIX', '!')

logger = logging.getLogger(__name__)

async def process_message(client, message: discord.Message):
    """
    Processes incoming messages, handling both command prefixes and mentions,
    then delegates command execution to the command handler.
    """
    # Check if the bot is mentioned
    if client.user in message.mentions:
        # Remove the mention part from the message content
        content_after_mention = message.content.replace(f'<@{client.user.id}>', '').strip()

        # Default to 'ask' command if no valid command follows the mention
        if not content_after_mention:
            command_name = 'ask'
            args = []
        else:
            # Split remaining content and treat the first word as the command
            args = content_after_mention.split()
            command_name = args.pop(0).lower()

            # If the command is not recognized, default to 'ask' and pass the full content as an argument
            if command_name not in COMMANDS:
                command_name = 'ask'
                args.insert(0, content_after_mention)  # Treat entire content as ask argument

        await handle_command(client, message, command_name, args)
        return

    # Handle prefixed commands using the configured PREFIX
    if message.content.startswith(PREFIX):
        command_name, *args = message.content[len(PREFIX):].strip().split()
        await handle_command(client, message, command_name, args)
    else:
        # Log non-command messages
        logger.info(f"Received non-command message from {message.author}: {message.content.strip().lower()}")
