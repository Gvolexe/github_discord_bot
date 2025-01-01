# main.py

import logging
import threading

from config import Config
from bot.discord_bot import DiscordBot
from flask_app.webhook import create_flask_app
from persistence.data_persistence import DataPersistence
from handlers.github_handlers import GitHubHandlers

def run_flask(app):
    """
    Runs the Flask application.

    Parameters:
    - app: The Flask application instance.
    """
    app.run(host="0.0.0.0", port=25578, debug=False)

def main():
    """
    The main function that initializes data persistence, Discord bot, and Flask server.
    It runs the Flask server in a separate daemon thread to allow the Discord bot to operate concurrently.
    """
    # Initialize data persistence
    data_persistence = DataPersistence(Config.DATA_STORE_FILE)
    data_persistence.load_data()

    # Initialize Discord Bot
    discord_bot = DiscordBot(Config, data_persistence)

    # Initialize GitHub Handlers with the Discord Bot instance
    github_handlers = GitHubHandlers(data_persistence, discord_bot)

    # Create Flask App
    flask_app = create_flask_app(Config, data_persistence, github_handlers)

    # Start Flask server in a separate daemon thread
    flask_thread = threading.Thread(target=run_flask, args=(flask_app,), daemon=True)
    flask_thread.start()
    logging.info("Flask server started in a separate thread.")

    # Run Discord Bot (blocking call)
    discord_bot.run()

if __name__ == "__main__":
    # Configure logging to include timestamp and log level
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
