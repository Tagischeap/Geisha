# events/on_ready.py
import discord
from discord.ext import tasks
from colorama import Fore, Style
from core.seasonal_handler import get_current_season 
import datetime
import asyncio

version = "11.10.25"
GUILD_ID = 85236952789442560  # Replace with the specific guild ID

async def on_ready(client):
    print("Executing on_ready from events/on_ready.py")
    print('----------------------------------------------------------------')
    print(Fore.YELLOW + f'Logged in as ' + Fore.GREEN + f'{client.user.name}' +
          Fore.YELLOW + f' (ID: ' + Fore.CYAN + f'{client.user.id}' + Fore.RESET + ')')
    print('Bot is connected to the following guilds:')

    for guild in client.guilds:
        print(Fore.CYAN + f' - {guild.name}' + Fore.WHITE + f' (ID: ' +
              Fore.CYAN + f'{guild.id}' + Fore.WHITE + f', Members: {guild.member_count})' + Style.RESET_ALL)
    
    print('----------------------------------------------------------------')
    
    # Set the bot's activity with version
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f'you. ({version})')
    )
    # Start the daily icon update task
    update_server_icon.start(client)
    await update_server_icon(client)

@tasks.loop(hours=24)
async def update_server_icon(client):
    guild = client.get_guild(GUILD_ID)
    if guild:
        season, icon_path = get_current_season()
        if season and icon_path:
            try:
                with open(icon_path, 'rb') as icon_file:
                    icon_data = icon_file.read()
                    await guild.edit(icon=icon_data)
                    print(f"Updated server icon for {season} season.")
            except discord.HTTPException as e:
                print(f"Failed to update server icon: {e}")

# Wait until midnight to start the task
@update_server_icon.before_loop
async def before_update_server_icon():
    now = datetime.datetime.now()
    next_midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    wait_time = (next_midnight - now).total_seconds()
    await asyncio.sleep(wait_time)