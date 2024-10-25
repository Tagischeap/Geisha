import os
import logging
from openai import AsyncOpenAI

# Initialize AsyncOpenAI client
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

logger = logging.getLogger(__name__)

async def get_openai_response(user_query):
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query}
            ],
            model="gpt-3.5-turbo",
        )
        # Correctly access the response content
        return response.choices[0].message.content  # Use dot notation instead of subscript
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "An error occurred while processing your request."
