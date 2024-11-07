# events/on_message.py

import discord
from core.message_handler import process_message
from events.on_message_react import react_to_message

async def on_message(client, message: discord.Message):
    """Listener for on_message events."""
    if message.author.bot:
        return  # Ignore messages from the bot itself
            # Check if the message is a reply to a bot's image message
    if message.reference:
        replied_message = await message.channel.fetch_message(message.reference.message_id)
        if replied_message.author == client.user and replied_message.attachments:
            # If the replied message is from the bot and contains an image, ignore
            return
            
    # Delegate message processing to the core handler
    await process_message(client, message)  # Pass both client and message

    # Add reactions based on specific words in the message
    await react_to_message(client, message)
