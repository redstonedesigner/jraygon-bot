"""
Utility functions for all commands.
"""
from discord.ext import vbu


async def respond(ctx: vbu.Context, msg: str):
    if isinstance(ctx, vbu.SlashContext):
        await ctx.interaction.followup.send(msg)
    else:
        await ctx.send(msg)
