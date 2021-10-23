from datetime import datetime

import discord

from cogs.utils.logging import format_date


async def message_log(message: discord.Message, reporter: discord.Member):
    embed = discord.Embed(
        title="New Message Report",
        description=f"```{message.content}```",
        colour=discord.Colour.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Message Author", value=message.author.mention)
    embed.add_field(name="Reported By", value=reporter.mention)
    return embed


async def user_log(user: discord.Member, reporter: discord.Member, reason: str):
    embed = discord.Embed(
        title="New User Report",
        description=f"```{reason}```",
        colour=discord.Colour.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Reported User", value=user.mention)
    embed.add_field(name="Submitted By", value=reporter.mention)
    return embed


async def dm(guild: discord.Guild, reporter: discord.Member):
    embed = discord.Embed(
        title="Report Received",
        description=f"""Hi {reporter.mention},
Thanks for your report!  It's been submitted to our moderators for review.

You may be contacted by a member of the moderation team with regard to further information.

Thanks,
Moderation Team
{guild.name}

PS: Spam/abuse of the report system will not be tolerated.""",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    return embed
