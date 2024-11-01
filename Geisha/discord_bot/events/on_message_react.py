# events/on_message_react.py
import discord
import random
import asyncio
import logging
from core.seasonal_handler import get_current_season, load_word_bank_and_emojis

logger = logging.getLogger(__name__)

async def react_to_message(client, message):
    try:
        if message.author == client.user:
            return

        # Determine the current season and load words and emojis
        season = get_current_season()
        if not season:
            return  # No seasonal event active

        bank_of_words, emoji_list = load_word_bank_and_emojis(season)

        # Check if the message contains any seasonal words
        message_words = set(word.lower() for word in message.content.split())
        if message_words.intersection(bank_of_words):
            # Check if the bot has already reacted with a seasonal emoji
            if not any(reaction.me for reaction in message.reactions if reaction.emoji in emoji_list):
                random_emoji = random.choice(emoji_list)
                await message.add_reaction(random_emoji)
                await asyncio.sleep(1)  # Rate limit prevention

    except discord.HTTPException as e:
        logger.error(f"Failed to add reaction: {e}")
