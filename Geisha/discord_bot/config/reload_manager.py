import importlib
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Initialize basic logging (if not imported from elsewhere)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Track last modified times for debounce
last_reload_times = {}
DEBOUNCE_TIME = 0.5  # seconds, short delay to avoid duplicates but allow quick reloads

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, client):
        self.client = client

    def on_modified(self, event):
        if event.event_type == 'modified' and event.src_path.endswith(".py"):
            # Convert file path to module name
            module_path = os.path.relpath(event.src_path, start=os.getcwd())
            module_name = module_path.replace(os.sep, ".")[:-3]  # Convert path to module name

            # Get the current time and check last reload time for debounce
            current_time = time.time()
            last_reload_time = last_reload_times.get(module_name, 0)

            # Reload only if enough time has passed since the last reload
            if current_time - last_reload_time > DEBOUNCE_TIME:
                try:
                    # Reload the module dynamically
                    module = importlib.import_module(module_name)
                    importlib.reload(module)
                    globals()[module_name] = module  # Update reference in globals
                    logger.info(f"Reloaded module: {module_name}")

                    # Update last reload time
                    last_reload_times[module_name] = current_time
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
