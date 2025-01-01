# bot/discord_bot.py

import discord
from discord.ext import commands
import asyncio
import logging

from bot.commands import setup_commands
from bot.utils import build_embed, get_color_and_emoji

class DiscordBot:
    """
    Encapsulates the Discord bot setup, event handling, and message management.
    """
    def __init__(self, config, data_persistence):
        """
        Initializes the DiscordBot instance.

        Parameters:
        - config (Config): Configuration instance.
        - data_persistence (DataPersistence): Data persistence instance.
        """
        self.config = config
        self.data_persistence = data_persistence
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
        self.setup_event_handlers()
        setup_commands(self.bot, self.config, self.data_persistence)

    def setup_event_handlers(self):
        """
        Sets up Discord bot event handlers, such as on_ready.
        """
        @self.bot.event
        async def on_ready():
            """
            Event handler for when the bot becomes ready.
            Syncs the command tree to ensure all hybrid commands are registered.
            """
            await self.bot.tree.sync()
            logging.info(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
            logging.info("Discord bot is ready.")

    async def send_or_edit(self, key, handler_name=None):
        """
        Sends a new Discord message or edits an existing one based on the unique key.
        Respects the current settings for event handlers and selected channel.

        Parameters:
        - key (str): The unique key for the "thing" (e.g., "push:abcd1234").
        - handler_name (str, optional): The name of the event handler that processed this event.
        """
        # Extract handler name from key
        handler = key.split(':')[0]

        # Check if handler is enabled
        handlers = self.data_persistence.get_data_store().get("handlers", {})
        handler_config = handlers.get(handler, {})
        if not handler_config.get("enabled", False):
            logging.info(f"Handler '{handler}' is disabled. Skipping send_or_edit for key '{key}'.")
            return

        # Retrieve data from DATA_STORE
        data = self.data_persistence.get_data_store().get(key, {})
        embed = build_embed(key, data, handler_name=handler_name)

        # Get the channel ID from handler configuration
        channel_id = handler_config.get("channel_id", self.config.DEFAULT_DISCORD_CHANNEL_ID)
        channel = self.bot.get_channel(channel_id)
        if not channel:
            logging.error(f"Channel {channel_id} for handler '{handler}' not found.")
            return

        try:
            message_map = self.data_persistence.get_message_map()
            if key in message_map:
                # Edit existing message
                message_id = message_map[key]
                try:
                    old_msg = await channel.fetch_message(message_id)
                    await old_msg.edit(embed=embed)
                    logging.info(f"Edited existing message for {key} in channel '{channel.name}'")
                except discord.NotFound:
                    # If message not found, send a new one
                    new_msg = await channel.send(embed=embed)
                    self.data_persistence.update_message_map(key, new_msg.id)
                    logging.info(f"Sent new message (old not found) for {key} in channel '{channel.name}'")
            else:
                # Send new message
                new_msg = await channel.send(embed=embed)
                self.data_persistence.update_message_map(key, new_msg.id)
                logging.info(f"Sent new message for {key} in channel '{channel.name}'")
        except discord.HTTPException as e:
            logging.error(f"Discord HTTPException for {key}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error for {key}: {e}")

    def run(self):
        """
        Starts the Discord bot.
        """
        self.bot.run(self.config.DISCORD_TOKEN)
