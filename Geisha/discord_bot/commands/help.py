# commands/help.py
import discord

name = 'help'
aliases = ['commands']
description = 'List all of my commands or info about a specific command.'
usage = 'help <command>'
cooldown = 5  # Cooldown of 5 seconds

async def execute(client, message, args, commands):
    prefix = '!'  # Set your command prefix here
    data = []

    # List all commands if no specific command is requested
    if not args:
        data.append("Here's a list of all my commands:")
        data.append(", ".join(f"`{cmd['name']}`" for cmd in commands.values()))  # Access command names
        data.append(f"\nYou can send `{prefix}help [command name]` to get info on a specific command!")

        try:
            # Attempt to send a DM to the user
            await message.author.send("\n".join(data))  
        except discord.Forbidden:
            # If DMs are disabled, send a message in the channel instead
            await message.channel.send(f"{message.author.mention}, I couldn't send you a DM. Please check your privacy settings or allow DMs from server members.")
        except Exception as e:
            # Handle other unexpected errors
            print(f"Could not send help DM to {message.author}.\nError: {e}")
            await message.channel.send("An unexpected error occurred while trying to send you a DM.")
        return

    # Handle specific command help
    name = args[0].lower()
    command = next(
        (cmd for cmd in commands.values() if cmd['name'] == name or name in cmd['aliases']),
        None
    )

    if not command:
        await message.channel.send(f"That's not a valid command, {message.author.mention}!")
        return

    data.append(f"> **Name:** {command['name']}")
    if command['aliases']:
        data.append(f"> **Aliases:** {', '.join(command['aliases'])}")
    if command['description']:
        data.append(f"> **Description:** {command['description']}")
    if command['usage']:
        data.append(f"> **Usage:** `{prefix}{command['name']} {command['usage']}`")

    data.append(f"> **Cooldown:** {command.get('cooldown', 3)} second(s)")

    try:
        await message.author.send("\n".join(data))
    except discord.Forbidden:
        # Directly send the public channel message without retrying the DM
        await message.channel.send(f"{message.author.mention}, I couldn't send you a DM. Please check your privacy settings.")
