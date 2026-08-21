# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import re
import smtplib
import sqlite3

import discord
from discord import ui

from emails.normal import SendNormal
from emails.spoofed import SendSpoofed
from utils.config import SMTP
from utils.theme import PURPLE, TAGLINE

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

SENDER_DOMAIN = SMTP.get("sender_domain", "noreply@YOUR_DOMAIN.com")


class choiseView(discord.ui.View):
    def __init__(self, owner_id, html_content, sender_email, subject, product_name, image_url, url):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.html_content = html_content
        self.sender_email = sender_email
        self.subject = subject
        self.product_name = product_name
        self.image_url = image_url
        self.url = url

    def _get_receiver_email(self, interaction):
        cursor.execute("SELECT email FROM licenses WHERE owner_id = ?", (str(interaction.user.id),))
        result = cursor.fetchone()
        return result[0] if result else None

    def _sending_embed(self, mode):
        return discord.Embed(
            title="📤 Sending Email...",
            description=f"Hang tight — your **{mode}** email is on its way! 💜",
            color=PURPLE,
        )

    def _confirmation_embed(self, mode):
        embed = discord.Embed(
            title="✅ Email Sent!",
            description=f"{mode} email sent successfully — check your inbox!",
            url=self.url,
            color=PURPLE,
        )
        embed.add_field(name="📦 Product", value=f"**{self.product_name}**", inline=False)
        if self.image_url and self.image_url != "None" and self.image_url.startswith("http"):
            embed.set_thumbnail(url=self.image_url)
        embed.set_footer(text=TAGLINE)
        return embed

    def _error_embed(self, message):
        return discord.Embed(title="🚫 Delivery Failed", description=message, color=PURPLE)

    def _missing_email_embed(self, interaction):
        return discord.Embed(
            title="🚫 No Email On File",
            description=f"{interaction.user.mention}, save your email in **Settings** first.",
            color=PURPLE,
        )

    def _swap_sender_domain(self):
        return re.sub(r"<[^>]+>", f"<{SENDER_DOMAIN}>", self.sender_email)

    @discord.ui.button(label="Spoofed Email", style=discord.ButtonStyle.danger)
    async def handle_spoofed(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

        receiver_email = self._get_receiver_email(interaction)
        if not receiver_email:
            return await interaction.response.edit_message(
                embed=self._missing_email_embed(interaction), view=None
            )

        await interaction.response.edit_message(embed=self._sending_embed("spoofed"), view=None)

        try:
            formatted_sender_email = self._swap_sender_domain()
            email_sender = SendSpoofed(
                formatted_sender_email, receiver_email, self.subject, self.html_content
            )
            email_sender.send_email()

            await interaction.edit_original_response(embed=self._confirmation_embed("Spoofed"), view=None)
            await interaction.followup.send(
                content=(
                    "💡 **Tip:** Spoofed domains don't always land. If the email never shows up, "
                    "try **Normal** instead — and check **Spam** (move it to Inbox so images load)."
                ),
                ephemeral=True,
            )
        except (smtplib.SMTPRecipientsRefused, smtplib.SMTPDataError) as e:
            print(f"Failed to send email: {e}")
            if isinstance(e, smtplib.SMTPDataError):
                embed = self._error_embed(
                    "Spoofed sending was blocked (unverified domain). Try **Normal Email** instead."
                )
            else:
                embed = self._error_embed("The email address was refused by the mail server.")
            await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label="Normal Email", style=discord.ButtonStyle.primary)
    async def handle_normal(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

        receiver_email = self._get_receiver_email(interaction)
        if not receiver_email:
            return await interaction.response.edit_message(
                embed=self._missing_email_embed(interaction), view=None
            )

        await interaction.response.edit_message(embed=self._sending_embed("normal"), view=None)

        try:
            formatted_sender_email = self._swap_sender_domain()
            email_sender = SendNormal(
                formatted_sender_email, receiver_email, self.subject, self.html_content
            )
            email_sender.send_email()

            await interaction.edit_original_response(embed=self._confirmation_embed("Normal"), view=None)
        except (smtplib.SMTPRecipientsRefused, smtplib.SMTPDataError) as e:
            print(f"Failed to send email: {e}")
            if isinstance(e, smtplib.SMTPDataError):
                embed = self._error_embed("Sending was blocked (unverified domain).")
            else:
                embed = self._error_embed("The email address was refused by the mail server.")
            await interaction.edit_original_response(embed=embed, view=None)
