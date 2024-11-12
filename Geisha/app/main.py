# app/main.py
from app.tasks import background_tasks, periodic_tasks

def start_app():
    print("Starting application...")
    # Start background tasks
    background_tasks.run_background_task()
    # Optionally, start periodic tasks or scheduled tasks here
    periodic_tasks.start_periodic_tasks()

if __name__ == "__main__":
    start_app()
