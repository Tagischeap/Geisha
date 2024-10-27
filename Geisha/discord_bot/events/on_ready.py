# events/on_ready.py
import discord
import logging

# Assuming logger is already set up globally
logger = logging.getLogger(__name__)

async def on_ready():
    """
    Event handler for when the bot is ready.
    """
    logger.info('----------------------------------------------------------------')
    logger.info(f'Logged in as {client.user.name}!')
    logger.info('----------------------------------------------------------------')
    version = "2410.25"  # Replace with the actual version if needed
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f'you. ({version})')
    )
