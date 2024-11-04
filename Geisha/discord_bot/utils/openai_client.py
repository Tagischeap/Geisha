# utils/openai_client.py

import openai  # Import added for `generate_image` function
import os
import aiohttp
import asyncio
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables and initialize logger
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)

# Set path relative to the script's location
system_message_path = os.path.join(os.path.dirname(__file__), 'system_message.txt')

# Retry parameters
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

async def get_openai_response(user_query: str, model_version: str = "gpt-4") -> str:
    """Fetches a response from the OpenAI API based on the user's query."""
    # Map provided version to the corresponding model
    model = {
        "default": "chatgpt-4o-latest",
        "3.5": "gpt-3.5-turbo",
        "4": "gpt-4",
        "turbo": "gpt-4-turbo",
        "4o": "gpt-4o",
        "o1": "o1-mini",
        "o1p": "o1-preview",
    }.get(model_version, model_version)  # Use provided model_version if not in dictionary
    logger.info(f"Requested model version: {model_version}")
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Attempt to fetch response from OpenAI API
            response = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content": open(system_message_path, "r").read()},
                    {"role": "user", "content": user_query}
                ],
                model=model,
            )
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

async def generate_image(prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1):
    print(f"generate_image: Generating image for prompt '{prompt}' with size {size}")  # Debug
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": n
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json_data) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"generate_image: Image URL received: {data['data'][0]['url']}")  # Debug
                    return data['data'][0]['url']
                else:
                    print(f"generate_image: Failed with status {response.status}")  # Debug
                    return None
    except Exception as e:
        print(f"generate_image: Error occurred - {e}")  # Debug for exception
        return None
