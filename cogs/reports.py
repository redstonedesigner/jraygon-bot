import asyncio

import discord
from discord.ext import commands, vbu

from cogs.utils import get_channel
from cogs.utils.logging import reports


class Reports(vbu.Cog):
    @commands.context_command(name="Report User")
    async def _context_command_report_user(
        self, ctx: vbu.SlashContext, user: discord.Member
    ):
        command = self.report_user
        await command.can_run(ctx)
        await ctx.invoke(command, user)

    @commands.command(name="report-user", add_slash_command=False)
    @commands.defer(ephemeral=True)
    @commands.guild_only()
    async def report_user(
        self, ctx: vbu.Context, user: discord.Member, reason: str = None
    ):
        channel = await get_channel(ctx.guild, "mod-reports")
        if reason is None:
            msg = f"Please state the reason for reporting {user.mention}."
            try:
                request_msg = await ctx.author.send(content=msg)
                await ctx.interaction.followup.send(
                    "Please check your messages to proceed."
                )
            except discord.Forbidden:
                await ctx.interaction.followup.send(
                    "Error: You need to enable DMs from server members to use this context command."
                )
                return
            try:
                check = (
                    lambda m: m.author.id == ctx.author.id
                    and m.channel.id == ctx.author.dm_channel.id
                )
                response_message = await self.bot.wait_for(
                    "message", check=check, timeout=30
                )
                reason = response_message.content
            except asyncio.TimeoutError:
                await request_msg.edit(content="Prompt timed out.")
                return
        log_msg = await reports.user_log(user, ctx.author, reason)
        await channel.send(embed=log_msg)
        dm_msg = await reports.dm(ctx.guild, ctx.author)
        await ctx.author.send(embed=dm_msg)

    @commands.context_command(name="Report message")
    async def _context_command_report_message(
        self, ctx: vbu.SlashContext, message: discord.Message
    ):
        command = self.report_message
        await command.can_run(ctx)
        await ctx.invoke(command, message)

    @commands.command(name="report-msg", add_slash_command=False)
    @commands.defer(ephemeral=True)
    @commands.guild_only()
    async def report_message(self, ctx: vbu.Context, message: discord.Message):
        channel = await get_channel(ctx.guild, "mod-reports")
        log_msg = await reports.message_log(message, ctx.author)
        await channel.send(embed=log_msg)
        try:
            dm_msg = await reports.dm(ctx.guild, ctx.author)
            await ctx.author.send(embed=dm_msg)
        except discord.Forbidden:
            pass
        await ctx.interaction.followup.send(content="Thanks for the report!")


def setup(bot: vbu.Bot):
    cog = Reports(bot)
    bot.add_cog(cog)
