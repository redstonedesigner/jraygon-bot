"""
Utility functions for all commands.
"""
import discord
from discord.ext import vbu


async def respond(ctx: vbu.Context, msg: str):
    if isinstance(ctx, vbu.SlashContext):
        await ctx.interaction.followup.send(msg)
    else:
        await ctx.send(msg)


async def get_channel(guild: discord.Guild, channel_name: str):
    for channel in guild.text_channels:
        if channel.name == channel_name:
            return channel
    return None
