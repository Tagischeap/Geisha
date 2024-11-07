# commands/help.py
import discord
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
prefix = os.getenv('PREFIX', '!')  # Retrieve prefix from environment or default to "!"

# Command metadata
name = 'help'
aliases = ['commands']
description = 'List all of my commands or get info about a specific command.'
usage = '<command>'
cooldown = 5

# Execute function for the help command
async def execute(client, message, args, commands):
    data = []

    # If no specific command requested, list all commands
    if not args:
        data.append("Here's a list of all my commands:")
        data.append(", ".join(f"`{cmd['name']}`" for cmd in commands.values()))
        data.append(f"\nYou can send `{prefix}help [command name]` to get info on a specific command.")
        
        try:
            await message.author.send("\n".join(data))
            if message.channel.type != discord.ChannelType.private:
                await message.reply("I've sent you a DM with all my commands!")
        except discord.Forbidden:
            await message.channel.send(f"{message.author.mention}, I couldn't send you a DM. Here’s the information:")
            await message.channel.send("\n".join(data))
        return

    # Get detailed help for a specific command
    command_name = args[0].lower()
    command = commands.get(command_name) or next(
        (cmd for cmd in commands.values() if command_name in cmd['aliases']), None
    )

    if not command:
        await message.reply("That's not a valid command!")
        return

    # Build detailed command information
    data.append(f"**Name:** {command['name']}")
    if command['aliases']:
        data.append(f"**Aliases:** {', '.join(command['aliases'])}")
    data.append(f"**Description:** {command['description']}")
    data.append(f"**Usage:** `{prefix}{command['name']} {command['usage']}`")
    data.append(f"**Cooldown:** {command['cooldown']} second(s)")

    await message.channel.send("\n".join(data))
