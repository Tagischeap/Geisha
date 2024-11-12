# main.py
import asyncio
from bot.main import start_bot
from web.app import start_server
from app.main import start_app

async def main():
    await asyncio.gather(
        start_app(),    # Starts core app tasks
        start_bot(),    # Starts the Discord bot
        start_server()  # Starts the web server
    )

if __name__ == "__main__":
    asyncio.run(main())
