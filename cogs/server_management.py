"""
Server management commands.
"""
from discord.ext import commands, vbu


class ServerManager(vbu.Cog):
    """
    Server management commands.
    """

    @commands.command(name='refresh-commands')
    @commands.is_owner()
    async def refresh_commands(self, ctx: vbu.Context):
        """
        An example ping command.
        """
        msg = "Refreshing slash commands..."

        if isinstance(ctx, vbu.SlashContext):
            await ctx.interaction.response.send_message(msg)
        else:
            await ctx.send(msg)

        await self.bot.register_application_commands(
            commands=None, guild=ctx.guild
        )
        added_commands = await self.bot.register_application_commands(
            guild=ctx.guild
        )


def setup(bot: vbu.Bot):
    """
    Register cog to bot
    :param bot: Bot instance
    """
    cog = ServerManager(bot)
    bot.add_cog(cog)
