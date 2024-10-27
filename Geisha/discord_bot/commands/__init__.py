import os
import importlib

commands = {}

def load_commands():
    """Dynamically loads all command modules."""
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith('.py') and filename != '__init__.py' and filename != 'handle_command.py':  # Exclude handle_command
            command_name = filename[:-3]  # Strip the '.py' extension
            module = importlib.import_module(f'commands.{command_name}')
            commands[command_name] = {
                'execute': module.execute,  # Ensure this line matches the function name
                'name': module.name,
                'aliases': module.aliases,
                'description': module.description,
                'usage': module.usage,
                'cooldown': getattr(module, 'cooldown', 3),  # Default to 3 seconds if not set
            }

load_commands()  # Call the function to load commands when the module is imported
