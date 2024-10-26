import discord
from utils.openai_client import get_openai_response  # Ensure you have this function implemented

# Command metadata
name = 'ask'
aliases = []
description = 'Ask a question to OpenAI.'
usage = '<your question>'
cooldown = 5  # Set your desired cooldown time

async def execute(client, message, args):
    """Executes the ask command by calling OpenAI with the user's query."""
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

async def handle_command(message):
    """Handles commands and checks for the 'ask' command."""
    prefix = '!'  # Define your command prefix here

    # Check if the message mentions her
    if client.user.mentioned_in(message):
        # Extract the content after the mention
        content_after_mention = message.content[len(message.mentions[0].mention):].strip()
        
        # Check if there's a question after the mention
        if content_after_mention:
            args = content_after_mention.split()  # Split the question into args
            await execute(client, message, args)  # Call the execute function for the 'ask' command
        else:
            await message.channel.send("How can I assist you? Please ask your question or use the '!ask' command.")
        return  # Exit after processing the mention

    # Check if the message starts with the command prefix
    if message.content.startswith(prefix):
        command_name = message.content[len(prefix):].split()[0]  # Extract the command name
        args = message.content[len(prefix) + len(command_name):].strip().split()  # Extract the arguments

        # Check if the command matches 'ask'
        if command_name == 'ask':
            await execute(client, message, args)  # Call the execute function for the 'ask' command
        else:
            await message.channel.send("I didn't understand that command. Please try '!ask <your question>'.")
