import discord
from discord.ext import commands

# Command metadata
name = 'purge'
aliases = ['delete']
description = 'Deletes messages in bulk (Admins only)'
usage = 'purge 10'

async def execute(self, message, args):
    """
    Executes the purge command, deleting messages in bulk.
    Usage: !purge 10
    """
    # Check if the user is a server admin
    if not message.author.guild_permissions.administrator:
        await message.reply("You don't have permission to use this command. (Admins only)")
        return

    # Parse the number of messages to delete
    try:
        amount = int(args[0]) + 1  # +1 to include the command message
    except (IndexError, ValueError):
        await message.reply("You need to specify the number of messages to delete (between 1 and 99).")
        return

    # Validate the amount
    if amount <= 1 or amount > 100:
        await message.reply("You need to input a number between 1 and 99.")
        return

    # Bulk delete messages and send confirmation
    deleted = await message.channel.purge(limit=amount)
    await message.channel.send(f"Deleted {len(deleted) - 1} messages.", delete_after=3)
