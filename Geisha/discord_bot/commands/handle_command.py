import importlib
import os

COMMANDS = {}

def load_commands():
    command_files = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.py') and f != '__init__.py' and f != 'handle_command.py']
    for command_name in command_files:
        try:
            module = importlib.import_module(f'commands.{command_name}')
            # Dynamically get the execute function by naming convention
            execute_func = getattr(module, 'execute', None)
            if execute_func:
                COMMANDS[f'!{command_name}'] = execute_func
        except ImportError as e:
            print(f"Error importing {command_name}: {e}")

load_commands()
