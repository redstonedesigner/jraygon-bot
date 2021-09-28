import discord
from discord.ext import commands, vbu


class Currency(vbu.Cog):

    @commands.group(invoke_without_command=True)
    async def balance(self, ctx: vbu.Context, member: discord.Member = None):
        """
        A command to retrieve the balance of yourself or another user.
        """
        member: discord.Member = member or ctx.author
        db = await vbu.Database.get_connection()
        result = await db.call(
            """SELECT user_id, balance FROM user_currency
            WHERE guild_id = $1 AND user_id = $2""",
            ctx.guild.id, member.id
        )
        if not result:
            await db.call(
                "INSERT INTO user_currency (guild_id, user_id, balance) VALUES ($1, $2, 0)",
                ctx.guild.id, member.id
            )
        result = await db.call(
            """SELECT user_id, balance FROM user_currency
            WHERE guild_id = $1 AND user_id = $2""",
            ctx.guild.id, member.id
        )
        await db.disconnect()
        result = result[0]

        if isinstance(ctx, vbu.SlashContext):
            await ctx.interaction.response.send_message(str(result['balance']))
        else:
            await ctx.send(str(result['balance']))

    @balance.command()
    async def add(self, ctx: vbu.Context, member: discord.Member, amount: int):
        db = await vbu.Database.get_connection()
        old = await db.call(
            """SELECT user_id, balance FROM user_currency
                        WHERE guild_id = $1 AND user_id = $2""",
            ctx.guild.id, member.id
        )
        old_balance = old[0]['balance']
        balance = old_balance + amount
        await db.call(
            """UPDATE user_currency SET balance = $1
            WHERE guild_id = $2 AND user_id = $3""",
            balance, ctx.guild.id, member.id
        )
        if isinstance(ctx, vbu.SlashContext):
            await ctx.interaction.response.send_message(
                f"Balance of {member.mention} adjusted by {amount}."
            )
        else:
            await ctx.send(f"Balance of {member.mention} adjusted by {amount}.")

    @balance.command()
    async def remove(self, ctx: vbu.Context, member: discord.Member, amount: int):
        db = await vbu.Database.get_connection()
        old = await db.call(
            """SELECT user_id, balance FROM user_currency
                        WHERE guild_id = $1 AND user_id = $2""",
            ctx.guild.id, member.id
        )
        old_balance = old[0]['balance']
        balance = old_balance - amount
        await db.call(
            """UPDATE user_currency SET balance = $1
            WHERE guild_id = $2 AND user_id = $3""",
            balance, ctx.guild.id, member.id
        )
        if isinstance(ctx, vbu.SlashContext):
            await ctx.interaction.response.send_message(
                f"Balance of {member.mention} adjusted by -{amount}."
            )
        else:
            await ctx.send(f"Balance of {member.mention} adjusted by -{amount}.")


def setup(bot: vbu.Bot):
    x = Currency(bot)
    bot.add_cog(x)
