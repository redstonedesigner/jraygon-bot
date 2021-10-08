"""
Utility functions related to currency management.
"""
from utils import database


async def _get(guild_id: int, user_id: int):
    session = await database.connect()
    result = await session.call(
        """SELECT user_id, balance FROM user_currency
        WHERE guild_id = $1 AND user_id = $2""",
        guild_id,
        user_id,
    )
    await database.disconnect(session)
    return result


async def _save(guild_id: int, user_id: int, balance: int):
    session = await database.connect()
    await session.call(
        """UPDATE user_currency SET balance = $1
        WHERE guild_id = $2 AND user_id = $3""",
        balance,
        guild_id,
        user_id,
    )
    await database.disconnect(session)


async def create(guild_id: int, user_id: int):
    session = await database.connect()
    await session.call(
        """INSERT INTO user_currency (guild_id, user_id, balance)
         VALUES ($1, $2, 0)""",
        guild_id,
        user_id,
    )
    await database.disconnect(session)


async def get(guild_id: int, user_id: int):
    row = await _get(guild_id, user_id)
    if not row:
        await create(guild_id, user_id)
        row = await _get(guild_id, user_id)
    result = row[0]
    return result


async def add(guild_id: int, user_id: int, amount: int):
    row = await _get(guild_id, user_id)
    result = row[0]
    balance = result["balance"] + amount
    await _save(guild_id, user_id, balance)


async def remove(guild_id: int, user_id: int, amount: int):
    row = await _get(guild_id, user_id)
    result = row[0]
    balance = result["balance"] - amount
    if balance < 0:
        return False, balance
    await _save(guild_id, user_id, balance)
    return True, balance
