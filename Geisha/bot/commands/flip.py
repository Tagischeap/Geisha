import random

# Command metadata for flip command
name = 'flip'
aliases = ['coinflip', 'f', 'flip a coin']
description = (
    'Flips a coin once or multiple times.\n'
    'Specify a number to flip multiple times (e.g., `flip 10`).'
)
usage = '<count>'
cooldown = 5
MAX_FLIPS = 100

def flip_coin(count=1):
    count = min(count, MAX_FLIPS)
    return [random.choice(["Heads", "Tails"]) for _ in range(count)]

def parse_flip_command(input_text):
    # Split input and check for number of flips
    parts = input_text.strip().split()
    count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1

    if count > MAX_FLIPS:
        return f"Sorry, you can only flip up to {MAX_FLIPS} coins at once."

    results = flip_coin(count)
    if count == 1:
        return f"The coin landed on: **{results[0]}**"
    else:
        result_str = ", ".join(results)
        return f"Fliped: **{result_str}**\nHeads: {results.count('Heads')}, Tails: {results.count('Tails')}"

# Execute function to reply with the flip results
async def execute(client, message, args):
    # Join args to pass as a single string to parse_flip_command
    result = parse_flip_command(f"flip {' '.join(args)}")
    await message.reply(result)
