from cogs.utils import database


async def accept(user_id: int):
    session = await database.connect()
    await session.call(
        """INSERT INTO user_settings (user_id, foaas_agreed)
        VALUES ($1, 1)
        ON CONFLICT (user_id)
        DO UPDATE SET foaas_agreed = 1""",
        user_id,
    )
    await database.disconnect(session)


async def check(user_id: int):
    session = await database.connect()
    row = await session.call(
        "SELECT user_id, foaas_agreed FROM user_settings WHERE user_id = $1",
        user_id,
    )
    await session.disconnect()
    try:
        result = row[0]
    except IndexError:
        return False
    if result["foaas_agreed"] != 1:
        return False
    return True
