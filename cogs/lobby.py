"""
Contains currency-based commands.
"""
import discord
from discord.ext import commands, vbu

from utils import lobby_vc, respond


class Lobby(vbu.Cog):
    """
    Commands to handle lobby VC systems.
    """

    @commands.group(invoke_without_command=True)
    async def lobby(self, ctx: vbu.Context):
        """
        Base command.
        :param ctx: Command Context
        """

    @lobby.command()
    @commands.defer()
    @commands.has_guild_permissions(manage_channels=True)
    async def create(
        self,
        ctx: vbu.Context,
        lobby: discord.VoiceChannel,
        private: discord.VoiceChannel,
        join_requests: discord.TextChannel,
        allowed_role: discord.Role,
    ):
        """
        Create a new lobby channel.
        """
        success = await lobby_vc.create(
            ctx.guild.id,
            lobby.id,
            private.id,
            join_requests.id,
            str(allowed_role.id),
        )
        if success:
            msg = "Success - Lobby system created."
        else:
            msg = "Failure - There is already a system tied to the specified lobby VC."
        await respond(ctx, msg)

    @lobby.command()
    @commands.defer()
    @commands.has_guild_permissions(manage_channels=True)
    async def delete(self, ctx: vbu.Context, lobby: discord.VoiceChannel):
        """
        Delete a lobby system.
        """
        await lobby_vc.delete(ctx.guild.id, lobby.id)
        await respond(ctx, msg="Lobby system deleted.")

    @lobby.command(name="add-role")
    @commands.defer()
    @commands.has_guild_permissions(manage_channels=True)
    async def add_role(
        self, ctx: vbu.Context, lobby: discord.VoiceChannel, role: discord.Role
    ):
        """
        Add new manager role to lobby channel.
        """
        success = await lobby_vc.add_role(ctx.guild.id, lobby.id, role.id)
        if success:
            msg = f"Success - {role.mention} can now manage requests to join."
        else:
            msg = "Failure - An unknown error occurred.  Please contact the developer if this persists."
        await respond(ctx, msg, private=True)

    @lobby.command(name="remove-role")
    @commands.defer()
    @commands.has_guild_permissions(manage_channels=True)
    async def remove_role(
        self, ctx: vbu.Context, lobby: discord.VoiceChannel, role: discord.Role
    ):
        """
        Remove manager role from lobby channel.
        """
        success = await lobby_vc.remove_role(ctx.guild.id, lobby.id, role.id)
        if success:
            msg = f"Success - {role.mention} can no longer manage requests to join."
        else:
            msg = "Failure - An unknown error occurred.  Please contact the developer if this persists."
        await respond(ctx, msg, private=True)

    @lobby.command(name="info")
    @commands.defer()
    @commands.has_guild_permissions(manage_channels=True)
    async def info(self, ctx: vbu.Context, lobby: discord.VoiceChannel):
        success, data, role_ids = await lobby_vc.get(ctx.guild.id, lobby.id)
        if not success:
            msg = (
                "There is no lobby system associated with that Voice Channel."
            )
            await respond(ctx, msg)
        else:
            roles = [ctx.guild.get_role(int(role_id)) for role_id in role_ids]
            role_mentions = ", ".join([role.mention for role in roles])
            msg = f"""Lobby channel information:
            Lobby: {ctx.guild.get_channel(data['lobby_channel_id']).mention}
            Private Channel: {ctx.guild.get_channel(data['private_channel_id']).mention}
            Request Channel: {ctx.guild.get_channel(data['request_channel_id']).mention}
            Allowed Roles: {role_mentions}
            """
            await respond(ctx, msg)

    @commands.Cog.listener("on_voice_state_update")
    async def handle_lobby_join(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if after.channel is None:
            pending_request = await lobby_vc.get_request_by_member_id(
                member.id
            )
            if pending_request:
                success, data, role_ids = await lobby_vc.get(
                    member.guild.id, before.channel.id
                )
                if not success:
                    return
                prior_request_channel = member.guild.get_channel(
                    data["request_channel_id"]
                )
                request_msg = await prior_request_channel.fetch_message(
                    pending_request[0]["message_id"]
                )
                await request_msg.delete()
                await lobby_vc.delete_request(member.id)
            return
        success, data, role_ids = await lobby_vc.get(
            member.guild.id, after.channel.id
        )
        if not success:
            return
        private_channel = member.guild.get_channel(data["private_channel_id"])
        request_embed = discord.Embed(
            title="Join Request",
            description=f"{member.mention} would like to join {private_channel.mention}",
            color=discord.Color.dark_orange(),
        )
        components = discord.ui.MessageComponents(
            discord.ui.ActionRow(
                discord.ui.Button(
                    label="Admit",
                    custom_id="LobbyVC_Admit",
                    style=discord.ButtonStyle.green,
                ),
                discord.ui.Button(
                    label="Reject",
                    custom_id="LobbyVC_Reject",
                    style=discord.ButtonStyle.red,
                ),
            )
        )
        request_channel = member.guild.get_channel(data["request_channel_id"])
        request_msg = await request_channel.send(
            embed=request_embed, components=components
        )
        await lobby_vc.create_request(
            data["lobby_channel_id"], request_msg.id, member.id
        )

    @commands.Cog.listener("on_component_interaction")
    async def handle_component(self, interaction: discord.Interaction):
        if not isinstance(interaction.component, discord.ui.button.Button):
            return
        if not interaction.component.custom_id.startswith("LobbyVC"):
            return
        await interaction.response.defer(ephemeral=True)
        join_request = await lobby_vc.get_request_by_message_id(
            interaction.message.id
        )
        if not join_request:
            msg = (
                "Unable to receive join request information.  OG MSG ID : "
                + str(interaction.message.id)
            )
            await interaction.followup.send(content=msg)
            return
        success, data, role_ids = await lobby_vc.get(
            interaction.guild.id, join_request[0]["lobby_vc_id"]
        )
        if not success:
            msg = "An error occurred."
        else:
            allowed_roles = [
                interaction.guild.get_role(int(role_id))
                for role_id in role_ids
            ]
            can_manage = False
            for i in allowed_roles:
                if i in interaction.user.roles:
                    can_manage = True
                    break
            if not can_manage:
                await interaction.followup.send(
                    content="You do not have permission to do that!",
                    ephemeral=True,
                )
                return
            member = interaction.guild.get_member(join_request[0]["user_id"])
            reason_prefix = (
                f"[{interaction.user.name}#{interaction.user.discriminator}]"
            )
            if interaction.component.custom_id == "LobbyVC_Admit":
                await lobby_vc.delete_request(member.id)
                channel = interaction.guild.get_channel(
                    data["private_channel_id"]
                )
                await member.move_to(
                    channel=channel,
                    reason=f"{reason_prefix} Join request accepted.",
                )
                msg = f"Admitted {member.mention} successfully."
                embed = discord.Embed(
                    title="Admitted",
                    description=f"{interaction.user.mention} admitted this member.",
                    color=discord.Color.dark_green(),
                )
                interaction.message.embeds.append(embed)
            elif interaction.component.custom_id == "LobbyVC_Reject":
                await lobby_vc.delete_request(member.id)
                await member.move_to(
                    channel=None,
                    reason=f"{reason_prefix} Join request rejected.",
                )
                msg = f"Rejected {member.mention} successfully."
                embed = discord.Embed(
                    title="Rejected",
                    description=f"{interaction.user.mention} rejected this member.",
                    color=discord.Color.dark_red(),
                )
                interaction.message.embeds.append(embed)
            else:
                msg = "Unknown interaction received."
        await interaction.message.edit(
            embeds=interaction.message.embeds, components=None
        )
        await interaction.followup.send(content=msg, ephemeral=True)


def setup(bot: vbu.Bot):
    """
    Registers command cog to bot.
    :param bot: Bot object
    """
    cog = Lobby(bot)
    bot.add_cog(cog)
