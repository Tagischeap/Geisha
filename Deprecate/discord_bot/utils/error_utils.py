import logging

logger = logging.getLogger(__name__)

async def send_discord_error(message, error_message):
    """Sends an error message to the Discord channel and logs the error."""
    logger.error(error_message)
    try:
        await message.channel.send("An error occurred. Please try again later.")
    except Exception as e:
        logger.error(f"Failed to send error message to Discord: {e}")
