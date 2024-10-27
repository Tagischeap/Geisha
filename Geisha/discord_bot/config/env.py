# config/env.py
import os
from dotenv import load_dotenv

def load_env():
    load_dotenv(dotenv_path='keys.env')
    return {
        'DISCORD_TOKEN': os.getenv('DISCORD_TOKEN'),
    }
