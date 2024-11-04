# 
import os
import aiohttp
import asyncio
import logging
from openai import AsyncOpenAI

# Load environment variables and initialize logger
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)

# Path to the external system message file
system_message_path = '/mnt/data/discord_bot/discord_bot/utils/system_message.txt'

# Retry parameters
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

async def get_openai_response(user_query: str) -> str:
    """Fetches a response from the OpenAI API based on the user's query."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Attempt to fetch response from OpenAI API
            response = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content":  open(system_message_path, "r").read()},
                    {"role": "user", "content": user_query}
                ],
                model="gpt-4o",
            )
            print(system_message_path)
            # Return the response content
            return response.choices[0].message.content

        except aiohttp.ClientError as e:
            logger.error(f"Network error on attempt {attempt} when calling OpenAI: {e}")
            if attempt == MAX_RETRIES:
                return "Network issue while contacting OpenAI. Please try again later."
        
        except asyncio.TimeoutError:
            logger.error(f"Timeout error on attempt {attempt} when calling OpenAI")
            if attempt == MAX_RETRIES:
                return "Request to OpenAI timed out. Please try again later."
        
        except Exception as e:
            logger.error(f"Unexpected error when calling OpenAI: {e}")
            return "An unexpected error occurred while processing your request."
        
        # Delay before retrying
        await asyncio.sleep(RETRY_DELAY)

    # Fallback response if all retries fail
    return "OpenAI service is currently unavailable. Please try again later."
