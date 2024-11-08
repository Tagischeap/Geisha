from apscheduler.schedulers.background import BackgroundScheduler

def start_periodic_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_task, 'interval', hours=24)
    scheduler.start()

def daily_task():
    print("Executing daily task...")

# Ensure the scheduler stops with the application
import atexit
atexit.register(lambda: scheduler.shutdown())
