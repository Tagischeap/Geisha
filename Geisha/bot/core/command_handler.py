# bot/core/command_handler.py

import logging
import discord
from discord.ext import commands
from core.command_loader import COMMANDS  # Import COMMANDS directly
from commands.dalle import process_queue  # Import process_queue function

logger = logging.getLogger(__name__)

async def handle_command(client, message: discord.Message, command_name: str, args: list):
    """
    Executes a command if found in the COMMANDS dictionary, considering aliases.
    """
    command = COMMANDS.get(command_name) or next(
        (cmd for cmd in COMMANDS.values() if command_name in cmd['aliases']), None
    )

    if command:
        try:
            if command_name == "help":  # Special handling for help command
                await command['execute'](client, message, args, COMMANDS)
            else:
                await command['execute'](client, message, args)
            logger.info(f"Executed command '{command_name}' with args: {args}")
        except Exception as e:
            logger.error(f"Error executing command '{command_name}': {e}", exc_info=True)
            await message.channel.send(f"An error occurred while executing `{command_name}`.")

            
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the necessary permissions to use this command.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Try again in {int(error.retry_after)} seconds.")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("Only the bot owner can use this command.")
    elif isinstance(error, commands.MissingRole):
        await ctx.send("You need the required role to use this command.")
    else:
        await ctx.send("An error occurred.")

def setup_queue(bot):
    """Ensures the process_queue task is started when the bot is ready."""
    print("setup_queue called")  # Debug to confirm setup_queue is called
    if not hasattr(bot, 'queue_task_started'):
        bot.queue_task_started = True
        print("setup_queue: Initializing queue...")  # Additional debug statement

        async def start_queue_processing():
            await bot.wait_until_ready()  # Ensure the bot is fully ready
            bot.loop.create_task(process_queue())  # Start process_queue task
            print("Queue processing started in command handler with setup_hook.")  # Debug confirmation

        bot.setup_hook = start_queue_processing
