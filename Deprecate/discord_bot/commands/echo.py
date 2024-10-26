name = 'echo'
aliases = ['say']
description = 'Repeat what is said'
usage = 'Hello.'

async def execute(client, message, args):
    fArg = message.content[len(message.content.split()[0]):].strip()  # Get the argument after the command
    await message.channel.send(fArg)
