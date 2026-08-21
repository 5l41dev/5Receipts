# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import json
import sqlite3
from datetime import datetime

import discord
from discord import ui
from faker import Faker

from addons.emailmodal import emailmodal
from utils.theme import PURPLE, TAGLINE

fake = Faker()


def clientid(config_path="config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        return int(config.get("client_role_id", 0)) if str(config.get("client_role_id", "")).isdigit() else 0


clientidd = clientid()

conn = sqlite3.connect("data.db")
cursor = conn.cursor()


def _dashboard_embed(emailtf, credentialstf):
    description = (
        f"Here's where your setup stands — fill in anything missing.\n\n"
        f"📧 Email = **{emailtf}**\n"
        f"👤 Credentials = **{credentialstf}**"
    )
    return discord.Embed(title="💜 Dashboard", description=description, color=PURPLE)


class custinfomodal(ui.Modal, title="Set up your Credentials"):
    Name = ui.TextInput(label="Name", style=discord.TextStyle.short, placeholder="Jordan Smith", required=True)
    street = ui.TextInput(label="Street", style=discord.TextStyle.short, placeholder="123 Main Street", required=True)
    city = ui.TextInput(label="City", style=discord.TextStyle.short, placeholder="New York", required=True)
    zipp = ui.TextInput(label="Zip", style=discord.TextStyle.short, placeholder="10001", required=True)
    country = ui.TextInput(label="Country", style=discord.TextStyle.short, placeholder="United States", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        owner_id = str(interaction.user.id)
        required_role_ids = [clientidd] if clientidd else []
        user_role_ids = [role.id for role in interaction.user.roles]

        if not required_role_ids or any(role_id in required_role_ids for role_id in user_role_ids):
            cursor.execute(
                """
                INSERT INTO licenses (owner_id, name, street, city, zipp, country, credentialstf)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(owner_id)
                DO UPDATE SET name = excluded.name, street = excluded.street, city = excluded.city,
                              zipp = excluded.zipp, country = excluded.country, credentialstf = excluded.credentialstf;
                """,
                (owner_id, self.Name.value, self.street.value, self.city.value,
                 self.zipp.value, self.country.value, "True"),
            )
            conn.commit()

            cursor.execute(
                "SELECT emailtf, credentialstf FROM licenses WHERE owner_id = ?",
                (str(interaction.user.id),),
            )
            license_data = cursor.fetchone()
            if license_data:
                emailtf, credentialstf = license_data

            await interaction.response.edit_message(embed=_dashboard_embed(emailtf, credentialstf))

            embed = discord.Embed(
                title="✅ Credentials Saved",
                description=f"Your details are locked in, {interaction.user.mention}.",
                color=PURPLE,
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="🚫 No Access",
                description=f"{interaction.user.mention}, you need an active plan to save credentials.",
                color=PURPLE,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class SettingsDrop(discord.ui.Select):
    def __init__(self, owner_id, user_roles):
        self.owner_id = owner_id
        options = [
            discord.SelectOption(label="Custom Info", description="Enter your details manually", emoji="📄"),
            discord.SelectOption(label="Random Info", description="Generate random details", emoji="🌐"),
            discord.SelectOption(label="Email", description="Update your email address", emoji="📧"),
        ]
        super().__init__(placeholder="Select an option to proceed...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )
            return

        if self.values[0] == "Custom Info":
            await interaction.response.send_modal(custinfomodal())
        elif self.values[0] == "Random Info":
            name = fake.name()
            street = fake.street_address()
            city = fake.city()
            zipp = fake.zipcode()
            country = "United States"
            owner_id = str(interaction.user.id)

            required_role_ids = [clientidd] if clientidd else []
            user_role_ids = [role.id for role in interaction.user.roles]

            if not required_role_ids or any(role_id in required_role_ids for role_id in user_role_ids):
                cursor.execute(
                    """
                    INSERT INTO licenses (owner_id, name, street, city, zipp, country, credentialstf)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(owner_id)
                    DO UPDATE SET name = excluded.name, street = excluded.street, city = excluded.city,
                                  zipp = excluded.zipp, country = excluded.country, credentialstf = excluded.credentialstf;
                    """,
                    (owner_id, name, street, city, zipp, country, "True"),
                )
                conn.commit()

                cursor.execute(
                    "SELECT emailtf, credentialstf FROM licenses WHERE owner_id = ?",
                    (str(interaction.user.id),),
                )
                license_data = cursor.fetchone()
                if license_data:
                    emailtf, credentialstf = license_data

                await interaction.response.edit_message(embed=_dashboard_embed(emailtf, credentialstf))

                embed = discord.Embed(
                    title="✅ Random Credentials Generated",
                    description=f"Fresh fake details saved for {interaction.user.mention}.",
                    color=PURPLE,
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="🚫 No Access",
                    description=f"{interaction.user.mention}, you need an active plan to save credentials.",
                    color=PURPLE,
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "Email":
            await interaction.response.send_modal(emailmodal())


class SettingsView(discord.ui.View):
    def __init__(self, owner_id, user_roles):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.user_roles = user_roles
        self.add_item(SettingsDrop(owner_id, user_roles))

    @discord.ui.button(label="Go Back")
    async def handle_leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            from addons.RegionalView import RegionSelectionView

            owner_id = interaction.user.id
            user_roles = interaction.user.roles
            embed = discord.Embed(
                title="💜 Dashboard",
                description="Pick a region to start generating — or head to settings.",
                color=PURPLE,
            )

            cursor.execute("SELECT expiry, key FROM licenses WHERE owner_id = ?", (str(interaction.user.id),))
            x = cursor.fetchone()
            if x:
                expiry_str, key = x
                extime = datetime.strptime(expiry_str, "%d/%m/%Y %H:%M:%S")
                now = datetime.now()
                delta = extime - now
                days_left = delta.days
                hours_left = delta.total_seconds() // 3600

                if extime < now:
                    embed.description = "🔒 Your plan expired — renew to keep cooking."
                elif key.startswith("LifetimeKey"):
                    embed.description = "🌍 Pick a region below. You're on **``Lifetime``** — enjoy! ✨"
                elif days_left > 0:
                    embed.description = (
                        "🌍 Pick a region below.\n"
                        f"You have **``{days_left} Days``** left on your plan."
                    )
                else:
                    embed.description = (
                        "🌍 Pick a region below.\n"
                        f"You have **``{int(hours_left)} Hours``** left on your plan."
                    )

                embed.set_footer(
                    text=f"{interaction.user}'s Panel • {TAGLINE}",
                    icon_url=interaction.user.avatar.url if interaction.user.avatar else None,
                )

            region_view = RegionSelectionView(owner_id, user_roles)
            await interaction.response.edit_message(embed=embed, view=region_view)
        else:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )
