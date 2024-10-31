import random
import re

# Command metadata for roll command
name = 'roll'
aliases = ['r', 'roll dice']
description = (
    'Rolls dice with basic syntax.\n'
    '`d6` will roll a single six-sided die.\n'
    '`4d20` will roll four twenty-sided dice.\n'
    '`1d6!` will make the roll explode.'
)
usage = '1d6'
cooldown = 5
MAX_AMMO = 201
MAX_SIZE = 9001

def roll_dice(amount, size, explode=False):
    rolls = []
    for _ in range(amount):
        roll = random.randint(1, size)
        rolls.append(roll)
        while explode and roll == size:
            roll = random.randint(1, size)
            rolls.append(roll)
    return rolls

def parse_roll_command(input_text):
    dice_pattern = r'(\d*)d(\d+)(!?)'
    matches = re.findall(dice_pattern, input_text.lower())

    if not matches:
        return "Invalid roll format."

    math_string = input_text
    single_roll = (len(matches) == 1 and (matches[0][0] == '' or matches[0][0] == '1'))
    broke = False

    for amount, size, explode in matches:
        amount = int(amount) if amount else 1
        size = int(size)
        explode = explode == '!'

        if size < 1:
            return '\n> 🎲 You rolled: **∞**'

        if size > MAX_SIZE or amount > MAX_AMMO:
            return random.choice(["That's too big for me to handle.", "*Rolls on floor*"])

        rolls = roll_dice(amount, size, explode)
        roll_str = " + ".join(map(str, rolls))
        math_string = math_string.replace(f"{amount}d{size}{'!' if explode else ''}", f"({roll_str})", 1)

    try:
        result = eval(math_string, {"__builtins__": None}, {})
        # Return simplified response if single die roll, otherwise include math_string
        if single_roll:
            return f">>> 🎲 You rolled: {result}"
        else:
            return f">>> 🎲 You rolled: {result}\n```js\n{math_string}\n```"
    except:
        return "Error: Invalid roll expression."

async def execute(client, message, args):
    input_text = "1d20" if not args else " ".join(args)
    result = parse_roll_command(input_text)
    await message.reply(result)
