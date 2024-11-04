import discord
import os
from dotenv import load_dotenv
from utils.openai_client import get_openai_response  # Ensure this function is implemented

# Load environment variables
load_dotenv()
prefix = os.getenv('PREFIX', '!')  # Retrieve command prefix from environment

# Command metadata
name = 'ask'
aliases = ['question', 'query']
description = 'Ask a question to OpenAI.'
usage = '<your question>'
cooldown = 5  # Cooldown time in seconds

async def execute(client, message, args):
    """
    Executes the ask command by calling OpenAI with the user's query.
    """

    rules_text = (""
    )
    if not args:
        await message.author.send(f"Please provide a question after the command, e.g., `{prefix}ask How are you?`")
        return

    user_query = " ".join(args)  # Combine arguments to form the user's question# Initialize the conversation chain
    
    # Collect the conversation chain
    conversation_chain = []
    current_message = message
    while current_message.reference:  # Traverse through previous replies
        replied_message = await message.channel.fetch_message(current_message.reference.message_id)
        if replied_message.author == client.user:
            conversation_chain.insert(0, f"Bot: {replied_message.content}")
        else:
            conversation_chain.insert(0, f"{replied_message.author.name}: {replied_message.content}")
        current_message = replied_message

    # Replace each user mention in user_query with the username
    for user in message.mentions:
        mention_str = f"<@{user.id}>"
        user_query = user_query.replace(mention_str, user.name)  # Replace mention with username

    # Create the prompt with rules, conversation history, and user query
    conversation_text = "\n".join(conversation_chain)
    full_prompt = f"{rules_text}\n\n{conversation_text}\n{message.author.name}: {user_query}\nBot: --Insert what bot says--"

    try:
        # Show typing indicator while processing the request
        async with message.channel.typing():
            response_text = await get_openai_response(full_prompt)  # Pass full_prompt to OpenAI
        await message.reply(response_text)  # Reply with the response from OpenAI
    except Exception as e:
        print(f"Error occurred when calling OpenAI: {e}")
        await message.author.send("An error occurred while processing your request. Please try again later.")


async def handle_mention(client, message):
    """
    Handles when the bot is mentioned in a message.
    """
    content_after_mention = message.content[len(message.mentions[0].mention):].strip()
    if content_after_mention:
        args = content_after_mention.split()  # Split the content into arguments
        await execute(client, message, args)
    else:
        await message.channel.send(f"How can I assist you? Please ask your question or use the `{prefix}ask` command.")

async def handle_command(client, message):
    """
    Handles commands and checks for the 'ask' command.
    """
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
