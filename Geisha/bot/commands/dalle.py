# commands/dalle.py

import aiohttp
import discord
import io
from utils.openai_client import generate_image

# Command metadata
name = 'dalle'
aliases = ['image', 'generate', 'draw']
description = 'Generate an image with DALL-E. Usage: !dalle <description>'
usage = '<description>'
cooldown = 30  # Cooldown time in seconds

async def process_queue(client):
    """Background task to process items in the queue."""
    print("Starting process_queue...")  # Initial debug message
    while True:
        print("Waiting for next item in queue...")  # Confirm the loop is active
        message, description = await client.task_queue.get()  # Use client.task_queue
        await message.remove_reaction('👀', client.user)
        print(f"process_queue: Processing request - {description}")  # Debug output for each item

        try:
            await message.add_reaction('✏️')
            image_url = await generate_image(description, size="1024x1024")
            if image_url == "policy_violation":
                await message.add_reaction('👄')  # Policy violation reaction
            elif image_url == "bad_request":
                await message.add_reaction('❓')  # Indicate a bad request

            if image_url:
                # Attempt to download the image asynchronously
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as response:
                        if response.status == 200:
                            data = await response.read()
                            file = discord.File(io.BytesIO(data), filename="image.png")
                            await message.reply(file=file)
                        else:
                            await message.reply(f"Here is your image: {image_url}")
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
        finally:
            await message.remove_reaction('✏️', client.user)
            client.task_queue.task_done()
            print("process_queue: Finished processing item, reaction removed.")

async def execute(client, message, args):
    if not args:
        await message.channel.send("Please provide a description for the image generation.")
        return

    description = " ".join(args)  # Combine args into a single prompt
    await client.task_queue.put((message, description))  # Queue using client.task_queue
    await message.add_reaction('👀')
    print(f"Request added to queue: {description}")  # Debug confirmation for queue
