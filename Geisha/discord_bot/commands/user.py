import discord
from discord.ext import commands

# Command metadata
name = 'user'
aliases = ['icon', 'pfp', 'avatar', 'avi']
description = 'Returns user information.'
usage = '!user [mention]'  # Usage string

# Execute function for the user command
async def execute(client, message, args):
    # Determine the target user
    if message.mentions:
        person = message.mentions[0]
    else:
        person = message.author

    # Send the user information to the channel
    await message.channel.send(
        f"""
        Username: {person.name}
        ID: {person.id}
        Avatar: {person.display_avatar.url}
        """
    )
