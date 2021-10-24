from random import randint

import discord
from discord.ext import commands, vbu, tasks

from cogs.utils import currency


class MessageRewards(vbu.Cog):
    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self._msg_user_ids = []
        self.purge_cache.start()

    def cog_unload(self) -> None:
        self.purge_cache.cancel()

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        user_id = message.author.id
        if user_id in self._msg_user_ids or message.author.bot:
            return
        self._msg_user_ids.append(user_id)
        await currency.add(message.guild.id, user_id, randint(5, 10))

    @tasks.loop(minutes=1.0)
    async def purge_cache(self):
        self._msg_user_ids = []


def setup(bot: vbu.Bot):
    cog = MessageRewards(bot)
    bot.add_cog(cog)
