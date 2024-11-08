# main.py at project root
from bot.main import start_bot
from web.server import start_server
from app.main import start_app

if __name__ == "__main__":
    start_app()      # Starts the core app (tasks, etc.)
    start_bot()      # Launches the Discord bot
    start_server()   # Runs the web server
