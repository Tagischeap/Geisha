import discord
from utils.openai_client import get_openai_response  # Ensure this function is implemented

# Command metadata
name = 'ask'
aliases = ['question', 'query']
description = 'Ask a question to OpenAI.'
usage = '<your question>'
cooldown = 5  # Cooldown time in seconds

async def execute(client, message, args):
    """
    Executes the ask command by calling OpenAI with the user's query.
    
    Parameters:
        client (discord.Client): The Discord client instance.
        message (discord.Message): The Discord message object.
        args (list): List of arguments after the command.
    """
    if not args:
        await message.author.send("Please provide a question after the command, e.g., `!ask How are you?`")
        return

    user_query = " ".join(args)  # Combine arguments to form the user's question
    try:
        response_text = await get_openai_response(user_query)  # Call OpenAI function
        await message.reply(response_text)  # Reply with the response from OpenAI
    except Exception as e:
        print(f"Error occurred when calling OpenAI: {e}")
        await message.author.send("An error occurred while processing your request. Please try again later.")

async def handle_mention(client, message):
    """
    Handles when the bot is mentioned in a message.
    
    Parameters:
        client (discord.Client): The Discord client instance.
        message (discord.Message): The Discord message object.
    """
    content_after_mention = message.content[len(message.mentions[0].mention):].strip()
    if content_after_mention:
        args = content_after_mention.split()  # Split the content into arguments
        await execute(client, message, args)
    else:
        await message.channel.send("How can I assist you? Please ask your question or use the `!ask` command.")

async def handle_command(client, message):
    """
    Handles commands and checks for the 'ask' command.
    
    Parameters:
        client (discord.Client): The Discord client instance.
        message (discord.Message): The Discord message object.
    """
    prefix = '!'  # Define your command prefix here

    # If the message mentions the bot
    if client.user.mentioned_in(message):
        await handle_mention(client, message)
        return  # Exit after processing the mention

    # If the message starts with the command prefix
    if message.content.startswith(prefix):
        command_name = message.content[len(prefix):].split()[0]  # Extract the command name
        args = message.content[len(prefix) + len(command_name):].strip().split()  # Extract the arguments

        # Check if the command matches 'ask' or its aliases
        if command_name in [name] + aliases:
            await execute(client, message, args)
        else:
            await message.channel.send(f"I didn't understand that command. Try `{prefix}ask <your question>`.")
