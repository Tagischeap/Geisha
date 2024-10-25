import logging
import discord  # Add this line
from utils.openai_client import get_openai_response
from utils.error_utils import send_discord_error

logger = logging.getLogger(__name__)

async def handler(client, message):
    logger.info(f"Message received: {message.content}")

    if message.author == client.user:
        return

    # Check if the message mentions the bot or is a reply
    if client.user in message.mentions or message.type == discord.MessageType.reply:
        user_query = message.content

        # If it's a reply, get the content of the replied message
        if message.type == discord.MessageType.reply:
            user_query = message.reference.resolved.content  # Get content of the message being replied to

        logger.info(f"Extracted user query: '{user_query}'")
        
        # Process the user's query using the OpenAI API
        try:
            response_text = await get_openai_response(user_query)
            try:
                await message.channel.send(response_text)
                logger.info("Response sent successfully.")
            except Exception as e:
                await send_discord_error(message, f"Error sending response message: {str(e)}")
            await message.add_reaction('👍')
        except Exception as e:
            await send_discord_error(message, f"Error with OpenAI request: {str(e)}")
