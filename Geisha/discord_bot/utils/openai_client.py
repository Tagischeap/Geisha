import os
import logging
from openai import AsyncOpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path='keys.env')

# Initialize AsyncOpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please check your .env file.")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

logger = logging.getLogger(__name__)

async def get_openai_response(user_query):
    """Fetches a response from the OpenAI API based on the user's query."""
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query}
            ],
            model="gpt-4",
        )
        # Correctly access the response content
        return response.choices[0].message.content  # Use dot notation instead of subscript
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "An error occurred while processing your request."
