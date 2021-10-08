# noqa
# pylint: skip-file
from discord.ext import vbu

from .warnings import Warnings


def setup(bot: vbu.Bot):
    cogs = [Warnings(bot)]
    for cog in cogs:
        bot.add_cog(cog)
