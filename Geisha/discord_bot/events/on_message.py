import logging
from commands import commands  # Import the commands dictionary

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

async def handle_command(client, message):
    """Handles commands and checks for the 'ask' command."""
    prefix = '!'  # Define your command prefix here

    # Check if the message mentions her
    if client.user.mentioned_in(message):
        content_after_mention = message.content[len(message.mentions[0].mention):].strip()
        
        if content_after_mention:
            args = content_after_mention.split()
            command_name = 'ask'  # Default command or customize as needed
            if command_name in commands:
                await commands[command_name]['execute'](client, message, args)
        else:
            await message.channel.send("How can I assist you? Please ask your question or use the '!ask' command.")
        return  # Exit after processing the mention

    # Check if the message starts with the command prefix
    if message.content.startswith(prefix):
        command_name = message.content[len(prefix):].split()[0]  # Extract the command name
        args = message.content[len(prefix) + len(command_name):].strip().split()  # Extract the arguments

        # Check if the command is recognized
        if command_name in commands:
            await commands[command_name]['execute'](client, message, args)  # Call the command's execute function
        else:
            await message.channel.send("I didn't understand that command. Please try '!ask <your question>'.")
