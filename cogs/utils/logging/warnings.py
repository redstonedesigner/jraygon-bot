"""
Contains messages related to logging warnings.
"""
from datetime import datetime

import discord

from . import format_date


async def issue_notify_user(member: discord.Member, reason: str):
    """
    Format DM to user on warning.
    :param member: Member being warned.
    :param reason: Reason for warning.
    :return:
    """
    message = f"""Hi {member.display_name},

    You have been warned in **{member.guild.name}**.
    The following reason was provided by a moderator: **{reason}**

    Continuing to violate the server's rules may result in further action."""
    embed = discord.Embed(
        title="You've received a warning!",
        description=message,
        color=discord.Color.yellow(),
        timestamp=datetime.utcnow(),
    )
    embed.set_author(name=member.guild.name)
    return embed


async def issue_notify_log(
    recipient: discord.Member, issuer: discord.Member, reason: str
):
    """
    Format moderation log entry for warning.
    :param recipient: Member who was warned.
    :param issuer: Member who issued warning.
    :param reason: Reason for warning.
    :return:
    """
    timestamp = datetime.utcnow()
    embed = discord.Embed(
        title="Warning Issued",
        color=discord.Color.yellow(),
        timestamp=timestamp,
    )
    embed.add_field(name="Issuer", value=issuer.mention)
    embed.add_field(name="Recipient", value=recipient.mention)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(
        name="Issuing Date",
        value=format_date(timestamp),
        inline=False,
    )
    return embed


async def clear_notify_log(issuer: discord.Member, recipient: discord.Member):
    """
    Format clear warnings log message.
    :param issuer: Member who cleared warnings.
    :param recipient: Member whose warnings were cleared.
    :return:
    """
    timestamp = datetime.utcnow()
    embed = discord.Embed(
        title="Warnings Cleared",
        color=discord.Color.dark_green(),
        timestamp=timestamp,
    )
    embed.add_field(name="User", value=recipient.mention)
    embed.add_field(name="Staff Member", value=issuer.mention)
    return embed


async def clear_notify_user(member: discord.Member):
    """
    Format DM to member.
    :param member: Member whose warnings were cleared.
    :return:
    """
    message = f"""Hi {member.display_name},

    All your warnings in **{member.guild.name}** have been cleared."""
    embed = discord.Embed(
        title="Warnings cleared!",
        description=message,
        color=discord.Color.dark_green(),
        timestamp=datetime.utcnow(),
    )
    embed.set_author(name=member.guild.name)
    return embed
