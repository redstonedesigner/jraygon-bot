"""
Contains logging functionality.
"""
import discord
from discord.ext import commands, vbu

from utils.logging import user, voice


class Logging(vbu.Cog):
    """
    Handles all logging.
    """

    @staticmethod
    async def _get_channel(guild: discord.Guild, channel_name: str):
        for channel in guild.text_channels:
            if channel.name == channel_name:
                return channel
        return None

    @commands.Cog.listener('on_member_join')
    async def log_member_join(self, member: discord.Member):
        channel = await self._get_channel(member.guild, 'joinleave-logs')
        embed = await user.join_message(member)
        await channel.send(embed=embed)

    @commands.Cog.listener('on_member_remove')
    async def log_member_leave(self, member: discord.Member):
        channel = await self._get_channel(member.guild, 'joinleave-logs')
        embed = await user.leave_message(member)
        await channel.send(embed=embed)

    @commands.Cog.listener('on_voice_state_update')
    async def log_voice_channel(
            self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
    ):
        if before.channel == after.channel:
            return
        elif before.channel is None:
            embed = await voice.connect_message(member, after.channel)
        elif after.channel is None:
            embed = await voice.disconnect_message(member, before.channel)
        else:
            embed = await voice.change_message(member, before, after)
        channel = await self._get_channel(member.guild, 'voice-log')
        await channel.send(embed=embed)


def setup(bot: vbu.Bot):
    """
    Registers command cog to bot.
    :param bot: Bot object
    """
    cog = Logging(bot)
    bot.add_cog(cog)
