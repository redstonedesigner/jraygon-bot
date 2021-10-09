"""
Utility functions for warning management.
"""
from datetime import datetime

from utils import database
from utils.logging import format_date


async def get_all(guild_id: int, user_id: int):
    """
    Fetch all warnings issued to a user.
    :param guild_id: Guild ID
    :param user_id: User ID
    :return:
    """
    session = await database.connect()
    result = await session.call(
        """SELECT warning_id, issuer_id, timestamp, reason FROM user_warnings
        WHERE guild_id = $1 AND user_id = $2 ORDER BY warning_id""",
        guild_id,
        user_id,
    )
    await database.disconnect(session)
    return result


async def create(guild_id: int, user_id: int, issuer_id: int, reason: str):
    """
    Create warning record.
    :param guild_id: Guild ID
    :param user_id: User ID
    :param issuer_id: Issuer ID
    :param reason: Reason for warning
    :return:
    """
    session = await database.connect()
    await session.call(
        """INSERT INTO user_warnings
        (guild_id, user_id, issuer_id, timestamp, reason)
        VALUES ($1, $2, $3, $4, $5)""",
        guild_id,
        user_id,
        issuer_id,
        format_date(datetime.utcnow()),
        reason,
    )
    await database.disconnect(session)


async def clear_user(guild_id: int, user_id: int):
    """
    Clear all warnings issued to a user.
    :param guild_id: Guild ID
    :param user_id: User ID
    :return:
    """
    session = await database.connect()
    await session.call(
        "DELETE FROM user_warnings WHERE guild_id = $1 AND user_id = $2",
        guild_id,
        user_id,
    )
    await database.disconnect(session)
