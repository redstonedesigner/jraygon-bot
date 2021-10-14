"""
Contains kicks cog.
"""
import discord
from discord.ext import commands, vbu

from cogs.utils import respond, get_channel
from cogs.utils.logging import kicks


class Kicks(vbu.Cog):
    """
    Warnings commands.
    """

    @commands.command()
    @commands.defer(ephemeral=True)
    @commands.has_any_role("Tavern Keeps", "Bar Keep", "Tavern Owner")
    async def kick(
        self, ctx: vbu.Context, member: discord.Member, reason: str
    ):
        if member.top_role >= ctx.author.top_role:
            msg = "You cannot kick that person!"
        else:
            msg = "Member kicked successfully."
            kick_msg = await kicks.kick_notify(ctx.guild, member, reason)
            kick_log = await kicks.kick_log(member, ctx.author, reason)
            try:
                await member.send(embed=kick_msg)
            except discord.Forbidden:
                kick_log.add_field(
                    name="Advisory",
                    value="User has DMs disabled.  As such, I was unable to deliver the kick notification.",
                    inline=False,
                )
            mod_log = await get_channel(ctx.guild, "mod-log")
            await mod_log.send(embed=kick_log)

        await respond(ctx, msg=msg)


def setup(bot: vbu.Bot):
    """
    Registers command cog to bot.
    :param bot: Bot object
    """
    cog = Kicks(bot)
    bot.add_cog(cog)
