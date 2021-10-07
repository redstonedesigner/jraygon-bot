"""
Contains voice logging messages.
"""
from datetime import datetime
from typing import Union

import discord


async def connect_message(
        member: discord.Member, channel: Union[discord.VoiceChannel, discord.StageChannel]
):
    embed = discord.Embed(
        title="User joined voice channel.",
        color=discord.Color.brand_green(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name='User', value=member.mention)
    embed.add_field(name='Channel', value=channel.mention)
    return embed


async def disconnect_message(
        member: discord.Member, channel: Union[discord.VoiceChannel, discord.StageChannel]
):
    embed = discord.Embed(
        title="User left voice channel.",
        color=discord.Color.brand_red(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name='User', value=member.mention)
    embed.add_field(name='Channel', value=channel.mention)
    return embed


async def change_message(
        member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
):
    embed = discord.Embed(
        title="User switched voice channel.",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name='User', value=member.mention, inline=False)
    embed.add_field(name='From', value=before.channel.mention, inline=True)
    embed.add_field(name='To', value=after.channel.mention, inline=True)
    return embed
