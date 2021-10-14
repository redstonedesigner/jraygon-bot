"""
Utility functions for all logging functions.
"""
from datetime import datetime

import discord


def format_username(member: discord.Member):
    """
    Format member information for log.
    :param member: Member to format log info for.
    :return:
    """
    template = "`{0.name}#{0.discriminator}` (`{0.id}`)"
    return template.format(member)


def format_date(timestamp: datetime):
    """
    Format timestamp to string.
    :param timestamp: Timestamp to format.
    :return:
    """
    return timestamp.strftime("%A, %d %B %Y %H:%M:%S")
