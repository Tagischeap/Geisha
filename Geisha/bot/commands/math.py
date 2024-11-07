# Command metadata for math command
import re

name = 'math'
aliases = ['calculate', 'solve', 'm', 'quickmaths', 'quick maths']
description = (
    'Solves basic arithmetic expressions.\n'
    'Supported operations: +, -, *, /, ^ (exponent).'
)
usage = '<expression>'
cooldown = 5

def evaluate_expression(math_string):
    try:
        result = eval(math_string, {"__builtins__": None}, {})
        return str(result) if result is not None else "Error: Invalid expression"
    except Exception as e:
        return f"Error: {str(e)}"

def parse_math_command(input_text):
    if not input_text.strip():
        return "Error: Please provide an expression to evaluate."
    
    result = evaluate_expression(input_text)
    # Only show "Error" if the result explicitly includes an error message
    if isinstance(result, str) and result.startswith("Error"):
        return result
    return f">>> Result: {result}"

# Execute function to handle math command
async def execute(client, message, args):
    try:
        # Use regex to remove any bot mention pattern (e.g., <@ID> or <@!ID>)
        command_text = re.sub(r"<@!?[0-9]+>", "", message.content).strip("!").strip().lower()

        # Debugging to observe the cleaned command_text
        print(f"[DEBUG] cleaned command_text: '{command_text}'")

        # Check if command_text matches "quickmaths" or "quick maths" directly
        if command_text in ['quickmaths', 'quick maths']:
            await message.reply("Two plus two is four. Minus one, that's three, quick maths.")
        else:
            # If args is empty, prompt for an expression
            if not args:
                await message.reply("Error: Please provide an expression to evaluate.")
            else:
                # Join args as a single expression string for evaluation
                input_text = " ".join(args).strip()
                result = parse_math_command(input_text)
                await message.reply(result)
    except Exception as e:
        # Log any errors and reply with a friendly error message
        print(f"[ERROR] Error executing command '{name}': {e}")
        await message.reply(f"An error occurred while executing {name}.")