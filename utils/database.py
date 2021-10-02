"""
Database utilities
"""
from discord.ext import vbu


async def connect() -> vbu.DatabaseConnection:
    return await vbu.Database.get_connection()


async def disconnect(session: vbu.DatabaseConnection):
    return await session.disconnect()
