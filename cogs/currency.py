"""
Contains currency-based commands.
"""
import discord
from discord.ext import commands, vbu


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
    async def view(self, ctx: vbu.Context, member: discord.Member = None):
        """
        A command to retrieve the balance of yourself or another user.
        """
        member: discord.Member = member or ctx.author
        database = await vbu.Database.get_connection()
        result = await database.call(
            """SELECT user_id, balance FROM user_currency
            WHERE guild_id = $1 AND user_id = $2""",
            ctx.guild.id,
            member.id,
        )
        if not result:
            await database.call(
                """INSERT INTO user_currency (guild_id, user_id, balance)
                 VALUES ($1, $2, 0)""",
                ctx.guild.id,
                member.id,
            )
        result = await database.call(
            """SELECT user_id, balance FROM user_currency
            WHERE guild_id = $1 AND user_id = $2""",
            ctx.guild.id,
            member.id,
        )
        await database.disconnect()
        result = result[0]

        if isinstance(ctx, vbu.SlashContext):
            await ctx.interaction.response.send_message(str(result["balance"]))
        else:
            await ctx.send(str(result["balance"]))

    @balance.command()
    async def add(self, ctx: vbu.Context, member: discord.Member, amount: int):
        """
        Add a specified amount of currency to a user.

        :param ctx: Command Context
        :param member: Member to add amount to
        :param amount: Amount to add to member
        """
        database = await vbu.Database.get_connection()
        old = await database.call(
            """SELECT user_id, balance FROM user_currency
                        WHERE guild_id = $1 AND user_id = $2""",
            ctx.guild.id,
            member.id,
        )
        old_balance = old[0]["balance"]
        balance = old_balance + amount
        await database.call(
            """UPDATE user_currency SET balance = $1
            WHERE guild_id = $2 AND user_id = $3""",
            balance,
            ctx.guild.id,
            member.id,
        )

        msg = f"Balance of {member.mention} adjusted by {amount}."

        if isinstance(ctx, vbu.SlashContext):
            await ctx.interaction.response.send_message(msg)
        else:
            await ctx.send(msg)

    @balance.command()
    async def remove(
            self, ctx: vbu.Context, member: discord.Member, amount: int
    ):
        """
        Remove a specified amount of currency from a user.

        :param ctx: Command Context
        :param member: Member to remove amount from
        :param amount: Amount to remove from member
        """
        database = await vbu.Database.get_connection()
        old = await database.call(
            """SELECT user_id, balance FROM user_currency
                        WHERE guild_id = $1 AND user_id = $2""",
            ctx.guild.id,
            member.id,
        )
        old_balance = old[0]["balance"]
        balance = old_balance - amount
        if balance < 0:
            msg = (
                f"Balance of {member.mention} may not go below 0."
                f" (Would be {balance})"
            )
        else:
            await database.call(
                """UPDATE user_currency SET balance = $1
                WHERE guild_id = $2 AND user_id = $3""",
                balance,
                ctx.guild.id,
                member.id,
            )
            msg = f"Balance of {member.mention} adjusted by -{amount}."

        if isinstance(ctx, vbu.SlashContext):
            await ctx.interaction.response.send_message(msg)
        else:
            await ctx.send(msg)


def setup(bot: vbu.Bot):
    """
    Registers command cog to bot.
    :param bot: Bot object
    """
    cog = Currency(bot)
    bot.add_cog(cog)
