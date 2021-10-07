"""
Contains user logging messages.
"""
from datetime import datetime

import discord

from utils.logging import format_date, format_username


async def join_message(member: discord.Member):
    display_name = format_username(member)
    embed = discord.Embed(
        title='A user has joined.',
        description=display_name + " has joined the server.",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    created_at = format_date(member.created_at)
    embed.add_field(name='Account Created', value=created_at)
    return embed


async def leave_message(member: discord.Member):
    display_name = format_username(member)
    embed = discord.Embed(
        title='A user has left.',
        description=display_name + " has left the server.",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    joined_at = format_date(member.joined_at)
    embed.add_field(name='Joined At', value=joined_at)
    return embed
