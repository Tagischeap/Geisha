import aiohttp
import discord
import os
import asyncio
import io
from utils.openai_client import generate_image  # Ensure this function is implemented

# Command metadata
name = 'dalle'
aliases = ['image', 'generate', 'draw']
description = 'Generate an image with DALL-E. Usage: !dalle <description>'
usage = '<description>'
cooldown = 30  # Cooldown time in seconds

# Create a queue to hold tasks
task_queue = asyncio.Queue()

async def process_queue():
    """Background task to process items in the queue."""
    print("Starting process_queue...")  # Initial debug message
    while True:
        print("Waiting for next item in queue...")  # Confirm the loop is active
        client, message, description = await task_queue.get()
        print(f"process_queue: Processing request - {description}")  # Debug output for each item

        image_url = None  # Initialize image_url to handle undefined cases
        
        try:
            # Add the "processing" reaction to the user's message
            await message.remove_reaction('👀', client.user)
            await message.add_reaction('✏️')
            print("process_queue: Added processing reaction.")  # Confirm reaction added

            # Generate image URL
            image_url = await generate_image(description, size="1024x1024")
            if not image_url:
                raise ValueError("Failed to generate image URL")  # Handle case if no URL returned

            print(f"process_queue: Image URL generated - {image_url}")  # Confirm URL generation
            
            # Attempt to download the image asynchronously
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        data = await response.read()
                        file = discord.File(io.BytesIO(data), filename="image.png")
                        await message.reply(file=file)  # Use reply here
                        print("process_queue: Image file sent as reply to Discord.")  # Confirm image sent
                    else:
                        await message.reply(f"Here is your image: {image_url}")
                        print("process_queue: Sent image URL due to download failure.")  # Debug on download failure
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
            print(f"process_queue: Error occurred while processing '{description}': {e}")  # Error debugging
        finally:
            # Remove the "processing" reaction after completion
            await message.remove_reaction('✏️', client.user)
            task_queue.task_done()
            print("process_queue: Finished processing item, reaction removed.")  # Confirm cleanup



async def execute(client, message, args):
    if not args:
        await message.channel.send("Please provide a description for the image generation.")
        return
    
    description = " ".join(args)  # Combine args into a single prompt
    
    # Add the task to the queue and confirm it was added
    await task_queue.put((client, message, description))
    await message.add_reaction('👀')
    print(f"Request added to queue: {description}")  # Debug confirmation for queue

# Ensure the queue starts processing when the bot is ready
def setup_queue(bot):
    """Ensures the process_queue task is started when the bot is ready."""
    if not hasattr(bot, 'queue_task_started'):
        bot.queue_task_started = True

        async def start_queue_processing():
            await bot.wait_until_ready()  # Ensure the bot is fully ready
            bot.loop.create_task(process_queue())  # Start process_queue task
            print("Queue processing started in command handler with setup_hook.")

        bot.setup_hook = start_queue_processing
