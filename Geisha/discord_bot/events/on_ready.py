# events/on_ready.py
import discord
from colorama import Fore, Style

version = "31.10.25"

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
