# commands/echo.py

name = 'echo'
aliases = ['say']
description = 'Repeat what is said'
usage = 'Hello.'

async def execute(client, message, args):
    """Echoes back the provided arguments."""
    response = " ".join(args)  # Join args into a single string
    await message.channel.send(response)
