# bot/commands.py

import discord
from discord.ext import commands
from discord import app_commands
import logging

def setup_commands(bot, config, data_persistence):
    """
    Sets up Discord bot commands related to event handler management.

    Parameters:
    - bot (commands.Bot): The Discord bot instance.
    - config (Config): Configuration instance.
    - data_persistence (DataPersistence): Data persistence instance.
    """
    @bot.hybrid_command(name='togglehandler', description='Toggle a specific event handler on or off.')
    @commands.has_permissions(administrator=True)
    async def togglehandler(ctx: commands.Context, handler_name: str):
        """
        Toggles a specific event handler on or off.

        Parameters:
        - ctx (commands.Context): The context of the command.
        - handler_name (str): The name of the handler to toggle.
        """
        handler_name = handler_name.lower()
        handlers = data_persistence.get_data_store().get("handlers", {})
        if handler_name not in handlers:
            await ctx.send(f"❌ Handler '{handler_name}' does not exist.")
            return
        current = handlers[handler_name].get("enabled", False)
        handlers[handler_name]["enabled"] = not current
        data_persistence.update_data_store("handlers", handlers)
        status = "✅ **enabled**" if not current else "❌ **disabled**"
        await ctx.send(f"📢 **Handler '{handler_name}' has been {status}.**")

    @togglehandler.error
    async def togglehandler_error(ctx: commands.Context, error):
        """
        Error handler for togglehandler command.

        Parameters:
        - ctx (commands.Context): The context of the command.
        - error (Exception): The exception raised.
        """
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Please provide a valid handler name.")

    @bot.hybrid_command(name='sethandlerchannel', description='Set the channel for a specific event handler.')
    @commands.has_permissions(administrator=True)
    async def sethandlerchannel(ctx: commands.Context, handler_name: str, channel: discord.TextChannel):
        """
        Sets the Discord channel for a specific handler.

        Parameters:
        - ctx (commands.Context): The context of the command.
        - handler_name (str): The name of the handler.
        - channel (discord.TextChannel): The Discord channel to assign.
        """
        handler_name = handler_name.lower()
        handlers = data_persistence.get_data_store().get("handlers", {})
        if handler_name not in handlers:
            await ctx.send(f"❌ Handler '{handler_name}' does not exist.")
            return
        handlers[handler_name]["channel_id"] = channel.id
        data_persistence.update_data_store("handlers", handlers)
        await ctx.send(f"📍 **Handler '{handler_name}' channel set to {channel.mention}.**")

    @sethandlerchannel.error
    async def sethandlerchannel_error(ctx: commands.Context, error):
        """
        Error handler for sethandlerchannel command.

        Parameters:
        - ctx (commands.Context): The context of the command.
        - error (Exception): The exception raised.
        """
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Please provide a valid text channel.")

    @bot.hybrid_command(name='listhandlers', description='List all event handlers with their status and assigned channels.')
    @commands.has_permissions(administrator=True)
    async def listhandlers(ctx: commands.Context):
        """
        Lists all event handlers with their enabled status and assigned channels.

        Parameters:
        - ctx (commands.Context): The context of the command.
        """
        handlers = data_persistence.get_data_store().get("handlers", {})
        if not handlers:
            await ctx.send("❌ No handlers are configured.")
            return
        embed = discord.Embed(title="📋 Event Handlers", color=discord.Color.blue())
        for handler, info in handlers.items():
            status = "Enabled ✅" if info.get("enabled", False) else "Disabled ❌"
            channel = bot.get_channel(info.get("channel_id", config.DEFAULT_DISCORD_CHANNEL_ID))
            channel_name = channel.mention if channel else f"Channel ID {info.get('channel_id')}"
            embed.add_field(name=handler.capitalize(), value=f"Status: {status}\nChannel: {channel_name}", inline=False)
        await ctx.send(embed=embed)

    @listhandlers.error
    async def listhandlers_error(ctx: commands.Context, error):
        """
        Error handler for listhandlers command.

        Parameters:
        - ctx (commands.Context): The context of the command.
        - error (Exception): The exception raised.
        """
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have permission to use this command.")
