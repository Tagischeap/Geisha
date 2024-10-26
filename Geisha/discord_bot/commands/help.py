import discord
from commands import commands  # Import the commands dictionary

name = 'help'
aliases = ['commands']
description = 'List all of my commands or info about a specific command.'
usage = 'help <command>'
cooldown = 5  # Cooldown of 5 seconds

async def execute(client, message, args):
    prefix = '!'  # Set your command prefix here
    data = []

    if not args:
        data.append("Here's a list of all my commands:")
        data.append(", ".join(f"`{cmd['name']}`" for cmd in commands.values()))  # Access command names
        data.append(f"\nYou can send `{prefix}help [command name]` to get info on a specific command!")

        try:
            await message.author.send("\n".join(data))  # Send DM with all commands
        except discord.Forbidden:
            await message.author.send("It seems like I can't DM you! Please check your DM settings to allow DMs from server members.")
        except Exception as e:
            print(f"Could not send help DM to {message.author}.\nError: {e}")
            await message.author.send("An error occurred while trying to send you a DM.")
        return

    name = args[0].lower()
    command = commands.get(name) or next((cmd for cmd in commands.values() if cmd['name'] == name or name in cmd['aliases']), None)

    if not command:
        await message.author.send("That's not a valid command!")
        return

    data.append(f"> **Name:** \n{command['name']}")

    if command['aliases']:
        data.append(f"> **Aliases:** \n{', '.join(command['aliases'])}")
    if command['description']:
        data.append(f"> **Description:** \n{command['description']}")
    if command['usage']:
        data.append(f"> **Usage:** \n`{prefix}{command['name']} {command['usage']}`")

    data.append(f"> **Cooldown:** \n{command.get('cooldown', 3)} second(s)")

    await message.author.send("\n".join(data))  # Send command details in DM
