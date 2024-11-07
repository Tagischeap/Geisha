# config/reload_manager.py
import importlib
import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Initialize basic logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Track last modified times and paths to improve debounce
last_reload_times = {}
DEBOUNCE_TIME = 1.5  # Increase debounce time for reliability

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, client):
        self.client = client

    def on_modified(self, event):
        if event.event_type == 'modified' and event.src_path.endswith(".py"):
            current_time = time.time()
            module_path = os.path.relpath(event.src_path, start=os.getcwd())
            module_name = module_path.replace(os.sep, ".")[:-3]

            # Check if main.py was modified for a full restart
            if event.src_path.endswith("main.py"):
                logger.info("Detected change in main.py, restarting bot...")
                python = sys.executable
                os.execv(python, [python] + sys.argv)

            # Use debounce to prevent double reloads
            last_reload = last_reload_times.get(module_name, 0)
            if current_time - last_reload > DEBOUNCE_TIME:
                try:
                    module = importlib.import_module(module_name)
                    importlib.reload(module)
                    logger.info(f"Reloaded module: {module_name}")
                    last_reload_times[module_name] = current_time  # Update last reload time
                except Exception as e:
                    logger.error(f"Error reloading module {module_name}: {e}")
            else:
                logger.info(f"Skipped reloading {module_name} due to debounce timing.")

def start_observer(client):
    """Starts the Watchdog observer for the entire project directory."""
    observer = Observer()
    observer.schedule(ReloadHandler(client), path='.', recursive=True)
    observer.start()
    
    logger.info("Reload Manager is active and watching for changes.")
    
    return observer
