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
    Processes messages, routing recognized commands and defaulting unrecognized commands to `ask`.
    """
    logger.debug(f"COMMANDS dictionary at runtime in process_message: {COMMANDS}")

    if client.user in message.mentions:
        content_after_mention = message.content.replace(f'<@{client.user.id}>', '').strip()
        if content_after_mention:
            args = content_after_mention.split()
            command_name = args.pop(0).lower()
        else:
            await message.channel.send("Please specify a command after mentioning me.")
            return

    elif message.content.startswith(PREFIX):
        command_name, *args = message.content[len(PREFIX):].strip().split()
    else:
        return  # Ignore non-command messages

    # Check if command_name exists in COMMANDS or any alias
    command = COMMANDS.get(command_name) or next(
        (cmd for cmd in COMMANDS.values() if command_name in cmd['aliases']), None
    )

    if command:
        await handle_command(client, message, command_name, args)
    else:
        # Fallback to 'ask' if command not found
        #logger.info(f"Unknown command '{command_name}', defaulting to 'ask'")
        
        # Check if 'ask' exists, reload if necessary
        if 'ask' not in COMMANDS:
            from core.command_loader import load_commands
            COMMANDS.update(load_commands())  # Reload COMMANDS if 'ask' is missing

        if 'ask' in COMMANDS:
            await COMMANDS['ask']['execute'](client, message, [command_name] + args)
        else:
            await message.channel.send("The `ask` command is not available.")
