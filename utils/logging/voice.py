"""
Contains voice logging messages.
"""
from datetime import datetime
from typing import Union

import discord


async def connect_message(
    member: discord.Member,
    channel: Union[discord.VoiceChannel, discord.StageChannel],
):
    """
    Format connection log message.
    :param member: Member that connected
    :param channel: Channel that member connected to
    :return:
    """
    embed = discord.Embed(
        title="User joined voice channel.",
        color=discord.Color.brand_green(),
        timestamp=datetime.utcnow(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Channel", value=channel.mention)
    return embed


async def disconnect_message(
    member: discord.Member,
    channel: Union[discord.VoiceChannel, discord.StageChannel],
):
    """
    Format user disconnect log message.
    :param member: Member that disconnected.
    :param channel: Channel that member disconnected from.
    :return:
    """
    embed = discord.Embed(
        title="User left voice channel.",
        color=discord.Color.brand_red(),
        timestamp=datetime.utcnow(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Channel", value=channel.mention)
    return embed


async def change_message(
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
):
    """
    Format channel switch message.
    :param member: Member that switched channels.
    :param before: VoiceState before switch.
    :param after: VoiceState after switch.
    :return:
    """
    embed = discord.Embed(
        title="User switched voice channel.",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow(),
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="User", value=member.mention, inline=False)
    embed.add_field(name="From", value=before.channel.mention, inline=True)
    embed.add_field(name="To", value=after.channel.mention, inline=True)
    return embed
