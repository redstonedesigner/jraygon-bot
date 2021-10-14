"""
Utility functions related to currency management.
"""
from utils import database


async def _get(guild_id: int, lobby_channel_id: int):
    session = await database.connect()
    result = await session.call(
        """SELECT * FROM lobby_vc
        WHERE guild_id = $1 AND lobby_channel_id = $2""",
        guild_id,
        lobby_channel_id,
    )
    await database.disconnect(session)
    return result


async def create(guild_id: int, lobby_channel_id: int, private_channel_id: int, request_channel_id: int, allowed_role_ids: str):
    """
    Create a new lobby VC record.
    :param guild_id: Guild ID
    :param lobby_channel_id: Channel users join to be admitted.
    :param private_channel_id: Channel users will be admitted to after approval.
    :param request_channel_id: Channel where requests will be sent.
    :param allowed_role_ids: A comma-delimited string of role IDs that can manage the lobby
    :return:
    """
    row = await _get(guild_id, lobby_channel_id)
    if row:
        return False
    session = await database.connect()
    await session.call(
        """INSERT INTO lobby_vc
        (guild_id, lobby_channel_id, private_channel_id, request_channel_id, allowed_role_ids)
        VALUES ($1, $2, $3, $4, $5)""",
        guild_id,
        lobby_channel_id,
        private_channel_id,
        request_channel_id,
        allowed_role_ids
    )
    await database.disconnect(session)
    return True


async def delete(guild_id: int, lobby_channel_id: int):
    session = await database.connect()
    await session.call(
        """DELETE FROM lobby_vc WHERE guild_id = $1 AND lobby_channel_id = $2""",
        guild_id,
        lobby_channel_id
    )
    await database.disconnect(session)
    return True


async def add_role(guild_id: int, lobby_channel_id: int, role_id: int):
    row = await _get(guild_id, lobby_channel_id)
    if not row:
        return False
    current_roles = row[0]['allowed_role_ids'].split(',')
    if role_id not in current_roles:
        current_roles.append(str(role_id))
    new_roles = ",".join(current_roles)
    session = await database.connect()
    await session.call(
        """UPDATE lobby_vc SET allowed_role_ids = $1
        WHERE guild_id = $2 AND lobby_channel_id = $3""",
        new_roles,
        guild_id,
        lobby_channel_id
    )
    await database.disconnect(session)
    return True


async def remove_role(guild_id: int, lobby_channel_id: int, role_id: int):
    row = await _get(guild_id, lobby_channel_id)
    if not row:
        return False
    current_roles = row[0]['allowed_role_ids'].split(',')
    if role_id in current_roles:
        current_roles.remove(str(role_id))
    new_roles = ",".join(current_roles)
    session = await database.connect()
    await session.call(
        """UPDATE lobby_vc SET allowed_role_ids = $1
        WHERE guild_id = $2 AND lobby_channel_id = $3""",
        new_roles,
        guild_id,
        lobby_channel_id
    )
    await database.disconnect(session)
    return True


async def get(guild_id: int, lobby_channel_id: int) -> (bool, dict, list):
    """
    Get a user's balance.
    :param lobby_channel_id: Specific channel to fetch.
    :param guild_id: Guild ID to fetch channel from.
    :return:
    """
    row = await _get(guild_id, lobby_channel_id)
    if not row:
        return False, {}, []
    result = row[0]
    role_ids = result['allowed_role_ids'].split(',')
    return True, result, role_ids


async def create_request(lobby_channel_id: int, message_id: int, user_id: int):
    session = await database.connect()
    await session.call(
        """INSERT INTO lobby_vc_join_request (lobby_vc_id, message_id, user_id)
        VALUES ($1, $2, $3)""",
        lobby_channel_id,
        message_id,
        user_id
    )
    await database.disconnect(session)


async def get_request_by_message_id(message_id: int):
    session = await database.connect()
    result = await session.call(
        """SELECT lobby_vc_id, user_id FROM lobby_vc_join_request WHERE message_id = $1""",
        message_id
    )
    await database.disconnect(session)
    return result


async def get_request_by_member_id(member_id: int):
    session = await database.connect()
    result = await session.call(
        """SELECT message_id FROM lobby_vc_join_request WHERE user_id = $1""",
        member_id
    )
    await database.disconnect(session)
    return result


async def delete_request(member_id: int):
    session = await database.connect()
    await session.call(
        """DELETE FROM lobby_vc_join_request WHERE user_id = $1""",
        member_id
    )
    await database.disconnect(session)
