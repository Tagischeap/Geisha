import time
from threading import Thread

def run_background_task():
    # Example background task that runs in a separate thread
    def task():
        while True:
            print("Running background task...")
            time.sleep(10)  # Simulate task interval

    # Start task in a new thread
    thread = Thread(target=task)
    thread.daemon = True  # Daemon threads automatically exit when main program exits
    thread.start()
