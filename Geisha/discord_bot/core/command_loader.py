# core/command_loader.py
import os
import importlib
import logging

logger = logging.getLogger(__name__)
commands = {}

def load_commands():
    """Dynamically loads all command modules."""
    commands_path = os.path.dirname(__file__) + '/../commands'
    for filename in os.listdir(commands_path):
        if filename.endswith('.py') and filename not in ('__init__.py', 'handle_command.py'):
            command_name = filename[:-3]
            module = importlib.import_module(f'commands.{command_name}')
            commands[command_name] = {
                'execute': module.execute,
                'name': module.name,
                'aliases': module.aliases,
                'description': module.description,
                'usage': module.usage,
                'cooldown': getattr(module, 'cooldown', 3),
            }
            logger.info(f"Loaded command: {command_name} with aliases {module.aliases}")
    return commands
