import os
import logging
from openai import AsyncOpenAI, OpenAIError

# Set up logging
logger = logging.getLogger(__name__)

# Initialize AsyncOpenAI client
client = None  # Initialize client as None

try:
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    logger.info("OpenAI client initialized successfully.")
except OpenAIError as e:
    logger.error("Failed to initialize OpenAI client: %s", e)

async def get_openai_response(user_query):
    if client is None:
        return "OpenAI client is not initialized. Please check your API key."
    
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query}
            ],
            model="gpt-3.5-turbo",
        )
        return response.choices[0].message.content  # Use dot notation instead of subscript
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "An error occurred while processing your request."
