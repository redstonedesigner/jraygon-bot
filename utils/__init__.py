"""
Utility functions for all commands.
"""
import discord
from discord.ext import vbu


async def respond(ctx: vbu.Context, msg: str = None, embed: discord.Embed = None, private: bool = False, allowed_mentions: discord.AllowedMentions = discord.AllowedMentions.none()):
    """
    Respond to a context with a given message.
    :param ctx: Context to respond to.
    :param msg: Message to respond with.
    :param embed: Embed to respond with.
    :param private: Whether the response should be private.
    :return:
    """
    if isinstance(ctx, vbu.SlashContext):
        await ctx.interaction.followup.send(content=msg, embed=embed, ephemeral=private, allowed_mentions=allowed_mentions)
    else:
        await ctx.send(content=msg, embed=embed, allowed_mentions=allowed_mentions)


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
