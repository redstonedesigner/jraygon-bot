"""
Database utilities
"""
from discord.ext import vbu


async def connect() -> vbu.DatabaseConnection:
    """
    Connect to the database.
    :return:
    """
    return await vbu.Database.get_connection()


async def disconnect(session: vbu.DatabaseConnection):
    """
    Disconnect a session.
    :param session: Session to disconnect.
    :return:
    """
    return await session.disconnect()
