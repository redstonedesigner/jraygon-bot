"""
Utility functions for all commands.
"""
import discord
from discord.ext import vbu


async def respond(ctx: vbu.Context, msg: str, private: bool = False):
    """
    Respond to a context with a given message.
    :param ctx: Context to respond to.
    :param msg: Message to respond to.
    :param private: Whether the response should be private.
    :return:
    """
    if isinstance(ctx, vbu.SlashContext):
        await ctx.interaction.followup.send(msg, ephemeral=private)
    else:
        await ctx.send(msg)


async def get_channel(guild: discord.Guild, channel_name: str):
    """
    GEt a specific text channel from a guild.
    :param guild: Guild to check
    :param channel_name: Channel name to search for
    :return:
    """
    for channel in guild.text_channels:
        if channel.name == channel_name:
            return channel
    return None
