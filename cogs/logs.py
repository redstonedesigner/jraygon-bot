"""
Contains logging functionality.
"""
import discord
from discord.ext import commands, vbu

from utils import get_channel
from utils.logging import user, voice


class Logging(vbu.Cog):
    """
    Handles all logging.
    """

    @commands.Cog.listener("on_member_join")
    async def log_member_join(self, member: discord.Member):
        """
        Logs member joining the guild.
        :param member: The member joining the guild.
        :return:
        """
        channel = await get_channel(member.guild, "joinleave-logs")
        embed = await user.join_message(member)
        await channel.send(embed=embed)

    @commands.Cog.listener("on_member_remove")
    async def log_member_leave(self, member: discord.Member):
        """
        Logs member leaving guild.
        :param member: The member leaving the guild.
        :return:
        """
        channel = await get_channel(member.guild, "joinleave-logs")
        embed = await user.leave_message(member)
        await channel.send(embed=embed)

    @commands.Cog.listener("on_voice_state_update")
    async def log_voice_channel(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState,
    ):
        """
        Log user changing voice channel.
        :param member: Member changing voice state.
        :param before: Voice state before update.
        :param after: Voice state after update.
        :return:
        """
        if before.channel == after.channel:
            return
        if before.channel is None:
            embed = await voice.connect_message(member, after.channel)
        elif after.channel is None:
            embed = await voice.disconnect_message(member, before.channel)
        else:
            embed = await voice.change_message(member, before, after)
        channel = await get_channel(member.guild, "voice-log")
        await channel.send(embed=embed)


def setup(bot: vbu.Bot):
    """
    Registers command cog to bot.
    :param bot: Bot object
    """
    cog = Logging(bot)
    bot.add_cog(cog)
