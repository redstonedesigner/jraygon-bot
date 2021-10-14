from datetime import datetime

import discord

from cogs.utils.logging import format_date


async def kick_notify(
    guild: discord.Guild, kicked: discord.Member, reason: str
):
    invite = await guild.rules_channel.create_invite(
        reason="Reinviting kicked user", max_uses=1
    )
    embed = discord.Embed(
        title="You've been kicked!",
        description=f"""Hi {kicked.display_name},
        
        You've been kicked from **{guild.name}**.
        The following reason was provided by a moderator: **{reason}**
        
        You can rejoin using the following invite: **{invite.url}**
        
        Please read the server rules again before interacting with the server.
        Failure to do so may result in further action being taken against you.""",
        timestamp=datetime.utcnow(),
        color=discord.Color.orange(),
    )
    embed.set_author(name=guild.name)
    return embed


async def kick_log(
    kicked: discord.Member, issuer: discord.Member, reason: str
):
    timestamp = datetime.utcnow()
    embed = discord.Embed(
        title="User Kicked", timestamp=timestamp, color=discord.Color.orange()
    )
    embed.add_field(name="Issuer", value=issuer.mention)
    embed.add_field(name="Recipient", value=kicked.mention)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(
        name="Issuing Date", value=format_date(timestamp), inline=False
    )
    return embed
