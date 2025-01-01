# config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Config:
    """
    Configuration class that holds all the necessary settings for the application.
    It fetches values from environment variables with default fallbacks.
    """
    # Discord Bot Token (replace with your actual token in production)
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

    # Discord Channel IDs for default and error messages
    DEFAULT_DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', 1284897403706806423))
    ERROR_DISCORD_CHANNEL_ID = int(os.getenv('ERROR_DISCORD_CHANNEL_ID', 1284897403706806423))

    # GitHub Webhook Secret for verifying incoming requests
    GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')

    # Additional Configuration Flags
    SEND_UNEXPECTED_EVENTS = os.getenv('SEND_UNEXPECTED_EVENTS', 'False').lower() in ['true', '1', 'yes']
    INCLUDE_HANDLER_INFO = os.getenv('INCLUDE_HANDLER_INFO', 'False').lower() in ['true', '1', 'yes']

    # File path for data persistence
    DATA_STORE_FILE = os.getenv('DATA_STORE_FILE', "data_store.json")
