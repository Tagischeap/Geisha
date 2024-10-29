# config/reload_manager.py
import importlib
import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Initialize basic logging (if not imported from elsewhere)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Track last modified times and paths for more effective debounce
last_reload_times = {}
DEBOUNCE_TIME = 1.0  # Increase debounce time to 1 second for more reliable filtering

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, client):
        self.client = client

    def on_modified(self, event):
        if event.event_type == 'modified' and event.src_path.endswith(".py"):
            # Handle main.py separately to restart the entire bot
            if event.src_path.endswith("main.py"):
                logger.info("Detected change in main.py, restarting bot...")
                python = sys.executable
                os.execv(python, [python] + sys.argv)  # Restart the process with the same arguments

            # Reload other modules dynamically
            module_path = os.path.relpath(event.src_path, start=os.getcwd())
            module_name = module_path.replace(os.sep, ".")[:-3]  # Convert path to module name

            # Get current time for debounce check
            current_time = time.time()
            last_reload_data = last_reload_times.get(module_name, (0, ""))

            # Only reload if enough time has passed and it's the same file path
            if (current_time - last_reload_data[0] > DEBOUNCE_TIME) or (last_reload_data[1] != event.src_path):
                try:
                    # Reload the module dynamically
                    module = importlib.import_module(module_name)
                    importlib.reload(module)
                    globals()[module_name] = module  # Update reference in globals
                    logger.info(f"Reloaded module: {module_name}")

                    # Update last reload time and path
                    last_reload_times[module_name] = (current_time, event.src_path)
                except Exception as e:
                    logger.error(f"Error reloading module {module_name}: {e}")

def start_observer(client):
    """Starts the Watchdog observer for the entire project directory."""
    observer = Observer()
    observer.schedule(ReloadHandler(client), path='.', recursive=True)
    observer.start()
    
    # Log that the reload manager is active
    logger.info("Reload Manager is active and watching for changes.")
    
    return observer
