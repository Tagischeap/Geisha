import discord
import random
import re

# Command metadata
name = 'roll'
aliases = ['r', 'math', 'm', 'sum', 'solve', 'quickmaths', 'qm']
description = (
    'Rolls dice with basic algebra syntax.\n'
    '`d6` will roll a single six-sided die.\n'
    '`4d20` will roll four twenty-sided dice.\n'
    '`1d6!` will make the roll explode.\n'
    'An exploding die is rolled again whenever its highest value is rolled.\n'
    'Operators can be added to roll additional dice or modify its result.\n'
    'Try `4d8! * 5 + d4^3d8! / (d6 + 5 - 2d4)`'
)
usage = '1d6'
cooldown = 5  # Set your desired cooldown time

async def execute(client, message, args):
    """Executes the roll command by rolling dice based on the provided syntax."""
    if not args:
        await message.channel.send("Please provide a roll command, e.g., `!roll 1d6`.")
        return

    fArg = " ".join(args)  # Join arguments to form the roll command
    dice_pattern = r'(\d*)d(\d+)(!?)'  # Regular expression for dice notation
    matches = re.findall(dice_pattern, fArg)

    roll_output = []
    total_roll = 0
    broke = False

    for match in matches:
        amount, size, exploding = match
        amount = int(amount) if amount else 1  # Default to 1 if no amount is specified
        size = int(size)

        if size < 1 or amount < 1:
            await message.channel.send("Invalid dice notation.")
            broke = True
            break

        # Roll the dice
        for _ in range(amount):
            roll = random.randint(1, size)
            total_roll += roll
            roll_output.append(str(roll))
            # Handle exploding dice
            while exploding == '!' and roll == size:
                roll = random.randint(1, size)
                total_roll += roll
                roll_output.append(str(roll))

    if not broke:
        await message.reply(f'You rolled: {total_roll}\nRolls: {", ".join(roll_output)}')
    else:
        await message.reply("Your roll command was invalid.")
