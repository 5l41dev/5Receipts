# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import json
import sqlite3
from datetime import datetime, timedelta

import discord
from discord import ui

from utils.theme import PURPLE, TAGLINE


def clientid(config_path="config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        return int(config.get("client_role_id", 0)) if str(config.get("client_role_id", "")).isdigit() else 0


conn = sqlite3.connect("data.db")
cursor = conn.cursor()


class emailmodal(ui.Modal, title="Set up your Email"):
    email = ui.TextInput(
        label="Email Address",
        style=discord.TextStyle.short,
        placeholder="Ex. youremail@gmail.com",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        clientidd = clientid()
        entered_email = self.email.value.lower()

        required_role_ids = [clientidd] if clientidd else []
        user_role_ids = [role.id for role in interaction.user.roles]

        if not required_role_ids or any(role_id in required_role_ids for role_id in user_role_ids):
            cursor.execute(
                "SELECT email, last_email_update FROM licenses WHERE owner_id = ?",
                (str(interaction.user.id),),
            )
            license_entry = cursor.fetchone()

            if license_entry:
                current_email, last_updated = license_entry
                if last_updated:
                    last_update_date = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
                    if datetime.now() - last_update_date < timedelta(days=7):
                        embed = discord.Embed(
                            title="⏳ Slow Down",
                            description="You can only change your email **once a week**.",
                            color=PURPLE,
                        )
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                cursor.execute(
                    "UPDATE licenses SET email = ?, last_email_update = ?, emailtf = 'True' WHERE owner_id = ?",
                    (entered_email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(interaction.user.id)),
                )
                conn.commit()

                cursor.execute(
                    "SELECT emailtf, credentialstf FROM licenses WHERE owner_id = ?",
                    (str(interaction.user.id),),
                )
                license_data = cursor.fetchone()
                if license_data:
                    emailtf, credentialstf = license_data

                description = (
                    f"Here's where your setup stands — fill in anything missing.\n\n"
                    f"📧 Email = **{emailtf}**\n"
                    f"👤 Credentials = **{credentialstf}**"
                )
                embed = discord.Embed(title="💜 Dashboard", description=description, color=PURPLE)
                await interaction.response.edit_message(embed=embed)

                embed = discord.Embed(
                    title="✅ Email Saved",
                    description=f"Delivery email set to `{entered_email}` for {interaction.user.mention}.",
                    color=PURPLE,
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="🚫 No Plan Found",
                    description=f"{interaction.user.mention}, you need an active plan to save an email.",
                    color=PURPLE,
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="🚫 No Access",
                description=f"{interaction.user.mention}, you don't have the role needed to save an email.",
                color=PURPLE,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
