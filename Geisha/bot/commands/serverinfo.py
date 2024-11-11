# commands/serverinfo.py

import discord

# Command metadata
name = 'serverinfo'
aliases = ['server', 'guildinfo']
description = 'Returns server information.'
usage = ''  # No arguments needed for server info

# Execute function for the server command
async def execute(client, message, args):
    # Check if the command is used in a server context
    if message.guild is None:
        await message.channel.send("This command can only be used in a server.")
        return

    guild = message.guild
    owner = guild.owner  # Attempt to get the server owner

    # Check if the owner is None and set a fallback message
    if owner is None:
        owner_info = "Owner information unavailable."
    else:
        owner_info = f"{owner} ({owner.id})"

    # Get the server icon URL or fallback if no icon is set
    icon_url = guild.icon.url if guild.icon else "No icon set for this server."

    # Send the server information to the channel
    await message.channel.send(
        f"""
        Server Name: {guild.name}
        Server ID: {guild.id}
        Owner: {owner_info}
        Member Count: {guild.member_count}
        Server Icon: {icon_url}
        """
    )