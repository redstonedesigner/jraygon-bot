"""
Utility functions for all logging functions.
"""
from datetime import datetime

import discord


def format_username(member: discord.Member):
    template = "`{0.name}#{0.discriminator}` (`{0.id}`)"
    return template.format(member)


def format_date(timestamp: datetime):
    return timestamp.strftime('%A, %d %B %Y %H:%M:%S')
