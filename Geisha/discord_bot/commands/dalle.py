import discord
import os
import requests
from utils.openai_client import generate_image  # Ensure this function is implemented

# Command metadata
name = 'dalle'
aliases = ['image', 'generate', 'draw']
description = 'Generate an image with DALL-E. Usage: !dalle <description>'
usage = '<description>'
cooldown = 5  # Cooldown time in seconds

async def execute(client, message, args):
    if not args:
        await message.channel.send("Please provide a description for the image generation.")
        return
    
    description = " ".join(args)  # Combine args into a single prompt

    try:
        # Add the "processing" reaction to the user's message
        await message.add_reaction('✏️')

        # Call the `generate_image` function from `openai_client`
        image_url = generate_image(description, size="1024x1024")
        
        # Attempt to download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            with open("image.png", 'wb') as f:
                f.write(response.content)
            
            # Send the image file
            with open("image.png", 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
            
            # Remove the image file after sending
            os.remove("image.png")
        else:
            # If download failed, send the image URL directly
            await message.channel.send(f"Here is your image: {image_url}")
    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")
    finally:
        # Remove the "processing" reaction after completion
        await message.remove_reaction('✏️', client.user)
