# core/command_loader.py
import os
import importlib
import logging

logger = logging.getLogger(__name__)
COMMANDS = {}  # Define COMMANDS globally for access in other modules

def load_commands():
    """Dynamically loads all command modules into COMMANDS."""
    commands_path = os.path.dirname(__file__) + '/../commands'
    for filename in os.listdir(commands_path):
        if filename.endswith('.py') and filename not in ('__init__.py', 'handle_command.py'):
            command_name = filename[:-3]
            try:
                module = importlib.import_module(f'commands.{command_name}')
                COMMANDS[command_name] = {
                    'execute': module.execute,
                    'name': module.name,
                    'aliases': module.aliases,
                    'description': module.description,
                    'usage': module.usage,
                    'cooldown': getattr(module, 'cooldown', 3),
                }
                logger.info(f"Loaded command: {command_name}")
            except Exception as e:
                logger.error(f"Failed to load command '{command_name}': {e}")

    if not COMMANDS:
        logger.error("No commands were loaded. Check command files for structure issues.")
    else:
        logger.info(f"All loaded commands: {list(COMMANDS.keys())}")
