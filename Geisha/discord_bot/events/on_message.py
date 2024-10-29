# events/on_message.py

import discord
from core.message_handler import process_message
from events.on_message_react import react_to_message

async def on_message(client, message: discord.Message):
    """Listener for on_message events."""
    if message.author.bot:
        return  # Ignore messages from the bot itself

    # Delegate message processing to the core handler
    await process_message(client, message)  # Pass both client and message

    # Add reactions based on specific words in the message
    await react_to_message(client, message)
