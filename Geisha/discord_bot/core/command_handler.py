import importlib
import os
import logging
import discord

logger = logging.getLogger(__name__)

COMMANDS = {}

def load_commands():
    """Loads command modules only if COMMANDS is empty to avoid duplicate loading."""
    if COMMANDS:  # Check if commands are already loaded
        logger.info("Commands already loaded; skipping duplicate load.")
        return

    commands_path = os.path.join(os.path.dirname(__file__), '../commands')
    command_files = [f[:-3] for f in os.listdir(commands_path) if f.endswith('.py') and f != '__init__.py']

    for command_name in command_files:
        try:
            module = importlib.import_module(f'commands.{command_name}')
            execute_func = getattr(module, 'execute', None)
            name = getattr(module, 'name', command_name)
            aliases = getattr(module, 'aliases', [])
            description = getattr(module, 'description', 'No description provided.')
            usage = getattr(module, 'usage', '')
            cooldown = getattr(module, 'cooldown', 3)  # Default cooldown

            if execute_func:
                COMMANDS[name] = {
                    'execute': execute_func,
                    'name': name,
                    'aliases': aliases,
                    'description': description,
                    'usage': usage,
                    'cooldown': cooldown
                }
                logger.info(f"Loaded command: {name}")
            else:
                logger.warning(f"No execute function found in {command_name}")
        
        except ImportError as e:
            logger.error(f"Error importing {command_name}: {e}")

async def handle_command(client, message: discord.Message, command_name: str, args: list):
    """
    Executes a command if found in the COMMANDS dictionary.
    """
    command = COMMANDS.get(command_name)

    if command:
        try:
            await command['execute'](client, message, args)
            logger.info(f"Executed command '{command_name}' with args: {args}")
        except Exception as e:
            logger.error(f"Error executing command '{command_name}': {e}")
            await message.channel.send(f"An error occurred while executing `{command_name}`.")
    else:
        logger.warning(f"Unknown command: '{command_name}' from {message.author}")
        await message.channel.send(f"Unknown command: `{command_name}`.")
