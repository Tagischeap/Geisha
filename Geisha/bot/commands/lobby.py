# bot/commands/lobby.py
name = 'lobby'
aliases = []
description = 'Creates a lobby for a drawing game'
usage = 'lobby'

import logging
import requests

# Ensure logging is configured (if not set globally)
logging.basicConfig(level=logging.INFO)

async def execute(client, message, args):
    """Creates a drawing game lobby and sends the invite link."""
    try:
        # Step 1: Fetch the lobby creation URL with a timeout
        discovery_response = requests.get("http://localhost:5000/api/get-lobby-url", timeout=5)
        discovery_response.raise_for_status()
        
        lobby_base_url = discovery_response.json().get("lobby_base_url")
        if not lobby_base_url:
            await message.channel.send("Failed to retrieve the lobby creation URL.")
            logging.error("No lobby_base_url found in the response.")
            return

        # Step 2: Use the retrieved URL to create a new lobby with a timeout
        response = requests.post(lobby_base_url, timeout=5)
        response.raise_for_status()
        
        lobby_data = response.json()
        lobby_url = lobby_data.get("lobby_url")
        if lobby_url:
            await message.channel.send(f"Join the drawing game lobby here: {lobby_url}")
        else:
            await message.channel.send("Lobby URL could not be retrieved. Please try again.")
            logging.error("No lobby_url found in the response.")
    
    # Handle specific exceptions
    except requests.Timeout:
        await message.channel.send("The request timed out. Please try again later.")
        logging.error("Timeout occurred during lobby URL request.")
        
    except requests.ConnectionError:
        await message.channel.send("Could not connect to the lobby server. Please try again later.")
        logging.error("Connection error occurred during lobby URL request.")
        
    except requests.RequestException as e:
        await message.channel.send("Failed to create a lobby. Please try again later.")
        logging.error("Request to create lobby failed", exc_info=e)
