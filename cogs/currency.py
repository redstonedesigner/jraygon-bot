"""
Contains currency-based commands.
"""
import discord
from discord.ext import commands, vbu

from cogs.utils import currency, respond


class Currency(vbu.Cog):
    """
    Currency-based commands are handled here.
    """

    @commands.group(invoke_without_command=True)
    async def balance(self, ctx: vbu.Context):
        """
        Balance commands.
        :param ctx: Command Context
        """

    @balance.command()
    @commands.defer()
    async def view(self, ctx: vbu.Context, member: discord.Member = None):
        """
        A command to retrieve the balance of yourself or another user.
        """
        member: discord.Member = member or ctx.author
        result = await currency.get(ctx.guild.id, member.id)

        msg = f"Current balance of {member.mention}: {result['balance']}"

        await respond(ctx, msg)

    @balance.command()
    @commands.defer()
    @commands.has_any_role("Tavern Owner", "Bar Keep", "Tavern Keep")
    async def add(self, ctx: vbu.Context, member: discord.Member, amount: int):
        """
        Add a specified amount of currency to a user.

        :param ctx: Command Context
        :param member: Member to add amount to
        :param amount: Amount to add to member
        """
        await currency.add(ctx.guild.id, member.id, amount)

        msg = f"Balance of {member.mention} increased by {amount}."

        await respond(ctx, msg)

    @balance.command()
    @commands.defer()
    @commands.has_any_role("Tavern Owner", "Bar Keep", "Tavern Keep")
    async def remove(
        self, ctx: vbu.Context, member: discord.Member, amount: int
    ):
        """
        Remove a specified amount of currency from a user.

        :param ctx: Command Context
        :param member: Member to remove amount from
        :param amount: Amount to remove from member
        """
        success, balance = await currency.remove(
            ctx.guild.id, member.id, amount
        )
        if not success:
            msg = (
                f"Balance of {member.mention} may not go below 0."
                f" (Would be {balance})"
            )
        else:
            msg = f"Balance of {member.mention} decreased by {amount}."

        await respond(ctx, msg)


def setup(bot: vbu.Bot):
    """
    Registers command cog to bot.
    :param bot: Bot object
    """
    cog = Currency(bot)
    bot.add_cog(cog)
