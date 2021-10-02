"""
A simple ping command.
"""
from discord.ext import commands, vbu


class PingCommand(vbu.Cog):
    """
    Contains ping command.
    """

    @commands.command()
    async def ping(self, ctx: vbu.Context):
        """
        An example ping command.
        """

        msg = f"Pong! {round(self.bot.latency * 1000)}ms"

        if isinstance(ctx, vbu.SlashContext):
            await ctx.interaction.response.send_message(msg)
        else:
            await ctx.send(msg)


def setup(bot: vbu.Bot):
    """
    Register cog to bot
    :param bot: Bot instance
    """
    cog = PingCommand(bot)
    bot.add_cog(cog)
