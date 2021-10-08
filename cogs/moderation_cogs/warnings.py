"""
Contains warnings cog.
"""
import discord
from discord.ext import commands, vbu

from utils import respond, warnings, get_channel
from utils.logging import warnings as log_warn


class Warnings(vbu.Cog):
    """
    Warnings commands.
    """

    @commands.group(name="warnings")
    async def warnings(self):
        """
        Placeholder function
        :return:
        """
        pass

    @warnings.command()
    @commands.defer()
    @commands.has_any_role("Tavern Keep", "Bar Keep", "Tavern Owner")
    async def view(self, ctx: vbu.Context, member: discord.Member):
        """
        View warnings issued to a user.
        :param ctx: Command context
        :param member: The user to view warnings for.
        :return:
        """
        warns = await warnings.get_all(member.guild.id, member.id)
        if len(warns) == 0:
            msg = "No warnings have been issued to this user."
        else:
            msg = "Warnings issued to user: \n\n"
            template = "{id} - {reason} ({timestamp}) [{issuer}]\n"
            for i in range(0, len(warns)):
                warn = warns[i]
                issuer = ctx.guild.get_member(warn["issuer_id"])
                temp_msg = (
                    template.replace("{id}", str(i + 1))
                        .replace("{reason}", warn["reason"])
                        .replace("{timestamp}", warn["timestamp"])
                        .replace("{issuer}", issuer.mention)
                )
                msg += temp_msg

        await respond(ctx, msg, private=True)

    @warnings.command()
    @commands.defer()
    @commands.has_any_role("Tavern Keep", "Bar Keep", "Tavern Owner")
    async def issue(
            self, ctx: vbu.Context, member: discord.Member, reason: str
    ):
        """
        Issue a warning to a user.
        :param ctx: Command context.
        :param member: Member being issued a warning.
        :param reason: The reason for the warning being issued.
        :return:
        """
        await warnings.create(ctx.guild.id, member.id, ctx.author.id, reason)
        try:
            user_msg = await log_warn.issue_notify_user(member, reason)
            await member.send(embed=user_msg)
            notify_failed = False
        except discord.Forbidden:
            notify_failed = True

        log_msg = await log_warn.issue_notify_log(member, ctx.author, reason)
        if notify_failed:
            log_msg.add_field(
                name="Advisory",
                value=(
                    "User has DMs disabled.  ",
                    "As such, I was unable to deliver ",
                    "the warning notification.",
                ),
            )

        log_channel = await get_channel(ctx.guild, "mod-log")
        await log_channel.send(embed=log_msg)

        await respond(ctx, "Warning successfully issued.")

    @warnings.command()
    @commands.defer()
    @commands.has_any_role("Bar Keep", "Tavern Owner")
    async def clear(self, ctx: vbu.Context, member: discord.Member):
        """
        Clear all warnings issued to a member.
        :param ctx: Command context.
        :param member: The member to clear all warnings from.
        :return:
        """
        await warnings.clear_user(ctx.guild.id, member.id)
        try:
            user_msg = await log_warn.clear_notify_user(member)
            await member.send(embed=user_msg)
            notify_failed = False
        except discord.Forbidden:
            notify_failed = True

        log_msg = await log_warn.clear_notify_log(ctx.author, member)
        if notify_failed:
            log_msg.add_field(
                name="Advisory",
                value=(
                    "User has DMs disabled.  ",
                    "As such, I was unable to deliver ",
                    "the clear notification.",
                ),
            )

        log_channel = await get_channel(ctx.guild, "mod-log")
        await log_channel.send(embed=log_msg)

        await respond(
            ctx, f"All warnings of {member.mention} cleared.", private=True
        )
