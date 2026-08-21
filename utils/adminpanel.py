# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import json
import sqlite3
from datetime import datetime, timedelta

import discord
from discord import ui

from utils.config import (
    CLIENT_ROLE_ID,
    EMU_ACCESS_ROLE_ID,
    PAPER_ACCESS_ROLE_ID,
    SALES_CHANNEL,
    SETUP_GUIDE_CHANNEL,
    VOUCH_CHANNEL,
    channel_mention,
)
from utils.database import get_connection
from utils.theme import PURPLE, TAGLINE

config = json.load(open("config.json", encoding="utf-8"))
conn = get_connection()
cursor = conn.cursor()


def _next_steps_field():
    setup = channel_mention(SETUP_GUIDE_CHANNEL)
    vouches = channel_mention(VOUCH_CHANNEL)
    steps = []
    if setup:
        steps.append(f"**»** Read the setup guide {setup} to get going.")
    if vouches:
        steps.append(f"**»** Drop a vouch in `+rep <10/10> <experience>` format {vouches}")
    if not steps:
        steps.append("**»** Set `setup_guide_channel` and `vouch_channel` in config.json to show next steps here.")
    return "\n".join(steps)


async def _grant_access(interaction, user, value):
    role_mapping = {
        "lftstandard": (1500, "LifetimeKey"),
        "1mstandard": (32, "1Month"),
        "lftpremium": (1500, "LifetimeKey"),
        "1mpremium": (32, "1Month"),
    }

    expiry_days, key_prefix = role_mapping[value]
    plan = "Lifetime" if expiry_days == 1500 else "1 Month"

    embed = discord.Embed(
        title="🎉 Access Granted!" if plan == "1 Month" else "🎉 Lifetime Access Granted!",
        description=f"Successfully added `{plan}` access to {user.mention}'s plan.",
        color=PURPLE,
    )
    embed.add_field(name="📚 Next Steps", value=_next_steps_field(), inline=False)
    embed.set_footer(text="✉️ Email can be changed once a week! • " + TAGLINE)
    if CLIENT_ROLE_ID.isdigit():
        client_role = user.guild.get_role(int(CLIENT_ROLE_ID))
        if client_role:
            try:
                await user.add_roles(client_role)
            except discord.Forbidden:
                pass  # Role assignment is best-effort — never block a grant on it.

    expiry_date = datetime.now() + timedelta(days=expiry_days)
    expiry_str = expiry_date.strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO licenses (owner_id, key, expiry, emailtf, credentialstf)
        VALUES (?, ?, ?, 'False', 'False')
        ON CONFLICT(owner_id) DO UPDATE SET
        key=excluded.key, expiry=excluded.expiry
        """,
        (str(user.id), f"{key_prefix}-{user.id}", expiry_str),
    )
    conn.commit()

    if SALES_CHANNEL.isdigit():
        channel = interaction.client.get_channel(int(SALES_CHANNEL))
        if channel:
            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                pass  # Announcement is best-effort — never block a grant on it.

    return embed


class adminDrop(discord.ui.Select):
    def __init__(self, owner_id, user):
        self.owner_id = owner_id
        self.user = user
        options = [
            discord.SelectOption(label="1 Month", description="Standard", emoji="🚀", value="1mstandard"),
            discord.SelectOption(label="Lifetime", description="Standard", emoji="🚀", value="lftstandard"),
        ]
        super().__init__(placeholder="Select an option to proceed...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )
            return

        # Acknowledge immediately so the interaction can never time out,
        # then finish the work with follow-ups.
        await interaction.response.defer(ephemeral=True)

        user = interaction.guild.get_member(self.user)
        if user is None:
            return await interaction.followup.send(
                "Couldn't find that user in this server.", ephemeral=True
            )

        try:
            await _grant_access(interaction, user, self.values[0])
        except Exception as e:
            return await interaction.followup.send(
                f"⚠️ Something went wrong while granting access: `{type(e).__name__}: {e}`",
                ephemeral=True,
            )

        await interaction.followup.send(
            "Access granted — confirmation posted!", ephemeral=True
        )


class PanelView(discord.ui.View):
    def __init__(self, owner_id, user):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.user = user

    @discord.ui.button(label="Information", emoji="ℹ️")
    async def handle_checktime(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)

        user = interaction.guild.get_member(self.user)
        if user is None:
            return await interaction.followup.send(
                "Couldn't find that user in this server.", ephemeral=True
            )
        embed = discord.Embed(title="ℹ️ User Information", color=PURPLE)
        user_found = False

        try:
            cursor.execute(
                "SELECT owner_id, key, expiry, email FROM licenses WHERE owner_id = ?",
                (str(user.id),),
            )
            license_info = cursor.fetchone()
        except sqlite3.Error as e:
            return await interaction.followup.send(
                f"⚠️ Couldn't read the database: `{e}`", ephemeral=True
            )

        if license_info:
            owner_id, key, expiry_str, email = license_info
            expiry_date = datetime.strptime(expiry_str, "%d/%m/%Y %H:%M:%S")
            current_date = datetime.now()
            remaining_days = (expiry_date - current_date).days

            embed.add_field(
                name="👤 User Details",
                value=(
                    f"**User:** <@{owner_id}>\n"
                    f"**Expiry:** {expiry_str} ``{remaining_days} Days``\n"
                    f"**Email:** `{email}`"
                ),
                inline=False,
            )
            user_found = True

        if not user_found:
            embed.add_field(name="❌ No Plan", value="User has no active plan on file.", inline=False)

        await interaction.followup.send(embed=embed, ephemeral=True)

    @discord.ui.button(label="Add Access", emoji="🔧")
    async def handle_addaccess(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

        view = discord.ui.View()
        view.add_item(adminDrop(self.owner_id, self.user))
        await interaction.response.send_message(content="", view=view, ephemeral=True)

    @discord.ui.button(label="Remove Access", emoji="🗑️")
    async def handle_removeaccess(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)

        user = interaction.guild.get_member(self.user)
        if user is None:
            return await interaction.followup.send(
                "Couldn't find that user in this server.", ephemeral=True
            )

        try:
            cursor.execute("DELETE FROM licenses WHERE owner_id = ?", (str(user.id),))
            conn.commit()
        except sqlite3.Error as e:
            return await interaction.followup.send(
                f"⚠️ Couldn't touch the database: `{e}`", ephemeral=True
            )

        role_ids = [CLIENT_ROLE_ID, PAPER_ACCESS_ROLE_ID, EMU_ACCESS_ROLE_ID]
        roles_to_remove = [
            role for role in user.roles if str(role.id) in role_ids
        ]
        if roles_to_remove:
            try:
                await user.remove_roles(*roles_to_remove)
            except discord.Forbidden:
                pass  # Role removal is best-effort.

        await interaction.followup.send(
            embed=discord.Embed(
                title="🗑️ Access Removed",
                description=f"The access for {user.mention} has been removed successfully.",
                color=PURPLE,
            ),
            ephemeral=True,
        )

    @discord.ui.button(label="Remove Email", emoji="📧")
    async def handle_removeemail(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)

        user = interaction.guild.get_member(self.user)
        if user is None:
            return await interaction.followup.send(
                "Couldn't find that user in this server.", ephemeral=True
            )

        try:
            cursor.execute(
                """
                UPDATE licenses
                SET email = NULL, last_email_update = NULL, emailtf = 'False'
                WHERE owner_id = ?
                """,
                (str(user.id),),
            )
            conn.commit()
        except sqlite3.Error as e:
            return await interaction.followup.send(
                f"⚠️ Couldn't touch the database: `{e}`", ephemeral=True
            )

        await interaction.followup.send(
            embed=discord.Embed(
                title="📧 Email Removed",
                description=f"The email for {user.mention} has been cleared.",
                color=PURPLE,
            ),
            ephemeral=True,
        )
