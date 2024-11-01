# config/env.py
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from keys.env
load_dotenv(dotenv_path='keys.env')

REQUIRED_VARS = ['DISCORD_TOKEN', 'OPENAI_API_KEY', 'PREFIX']

def load_and_validate_env_vars():
    """Loads and validates essential environment variables."""
    missing_vars = []

    for var in REQUIRED_VARS:
        if not os.getenv(var):
            missing_vars.append(var)
            logger.error(f"Environment variable {var} is missing.")

    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}. Check your keys.env file.")
    
    return {var: os.getenv(var) for var in REQUIRED_VARS}
