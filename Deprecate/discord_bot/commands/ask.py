import discord
from utils.openai_client import get_openai_response  # Ensure you have this function implemented

name = 'ask'
aliases = []
description = 'Ask a question to OpenAI.'
usage = '<your question>'
cooldown = 5  # Set your desired cooldown time

async def execute(client, message, args):
    if not args:
        await message.author.send("Please provide a question after the command.")
        return

    user_query = " ".join(args)  # Join arguments to form the query
    try:
        response_text = await get_openai_response(user_query)  # Call OpenAI function
        await message.reply(response_text)  # Reply with the response
    except Exception as e:
        print(f"Error occurred when calling OpenAI: {e}")
        await message.author.send("An error occurred while processing your request.")
