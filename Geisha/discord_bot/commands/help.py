# commands/help.py
import discord
import os
from dotenv import load_dotenv
from commands import commands  # Import commands dictionary directly

# Load environment variables
load_dotenv()
prefix = os.getenv('PREFIX', '!')  # Retrieve prefix from environment or default to "!"

name = 'help'
aliases = ['commands']
description = 'List all of my commands or info about a specific command.'
usage = 'help <command>'
cooldown = 5  # Cooldown of 5 seconds

async def execute(client, message, args):
    data = []

    # List all commands if no specific command is requested
    if not args:
        data.append("Here's a list of all my commands:")
        
        if commands:
            data.append(", ".join(f"`{cmd['name']}`" for cmd in commands.values()))
            data.append(f"\nYou can send `{prefix}help [command name]` to get info on a specific command!")
        else:
            data.append("No commands are currently available.")
        
        # Attempt to send a DM to the user with help information
        try:
            await message.author.send("\n".join(data))  
            await message.reply("I've sent you a DM with all my commands!") if message.channel.type != 'dm' else None
        except discord.Forbidden:
            await message.channel.send(f"{message.author.mention}, I couldn't send you a DM. Here’s the information you requested:\n" + "\n".join(data))
        except Exception as e:
            print(f"Unexpected error while sending help DM to {message.author}: {e}")
            await message.channel.send("An unexpected error occurred while trying to send help information.")
        return

    # Handle specific command help
    name = args[0].lower()
    command = commands.get(name) or next(
        (cmd for cmd in commands.values() if name in cmd['aliases']),
        None
    )

    if not command:
        await message.reply("That's not a valid command!")
        return

    data.append(f"**Name:** {command['name']}")
    if command['aliases']:
        data.append(f"**Aliases:** {', '.join(command['aliases'])}")
    if command['description']:
        data.append(f"**Description:** {command['description']}")
    if command['usage']:
        data.append(f"**Usage:** `{prefix}{command['name']} {command['usage']}`")

    data.append(f"**Cooldown:** {command['cooldown']} second(s)")

    # Send detailed command information in the channel
    await message.channel.send("\n".join(data))
