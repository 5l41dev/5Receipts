# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import asyncio
import sqlite3
from datetime import datetime

import discord
from discord.ext import commands

from addons.RegionalView import RegionSelectionView
from utils.theme import PURPLE, TAGLINE


class GenerateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

    @discord.app_commands.command(name="generate", description="Generate 1:1 receipts")
    async def receiptgen(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_roles = interaction.user.roles

        embed = discord.Embed(
            title="💜 Receipt Generator",
            description="🔒 No access found — grab a plan to start cooking.",
            color=PURPLE,
        )

        self.cursor.execute(
            "SELECT expiry, key FROM licenses WHERE owner_id = ?", (str(user_id),)
        )
        license = self.cursor.fetchone()

        if license:
            expiry_str, key = license
            expiry_date = datetime.strptime(expiry_str, "%d/%m/%Y %H:%M:%S")
            now = datetime.now()
            delta = expiry_date - now
            days_left = delta.days
            hours_left = delta.total_seconds() // 3600

            if expiry_date < now:
                embed.description = "❌ Your subscription has expired — renew to keep cooking."
            elif key.startswith("LifetimeKey"):
                embed.description = (
                    "🌍 Pick a region below to start generating.\n"
                    "You're on a **``Lifetime``** plan — enjoy the ride. ✨"
                )
            elif days_left > 0:
                embed.description = (
                    "🌍 Pick a region below to start generating.\n"
                    f"You have **``{days_left} Days``** left on your plan. ⏳"
                )
            else:
                embed.description = (
                    "🌍 Pick a region below to start generating.\n"
                    f"You have **``{int(hours_left)} Hours``** left on your plan. ⏳"
                )

        embed.set_footer(
            text=f"{interaction.user}'s Panel • {TAGLINE}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None,
        )
        region_view = RegionSelectionView(user_id, user_roles)
        await interaction.response.send_message(embed=embed, view=region_view)

        # Timeout cleanup
        await asyncio.sleep(160)
        follow_up_embed = discord.Embed(
            title="⏰ Menu Timed Out",
            description=(
                "The menu closed itself after sitting idle.\n"
                "🔄 Type `/generate` again whenever you're ready."
            ),
            color=PURPLE,
        )
        follow_up_embed.set_footer(
            text=f"{interaction.user}'s Panel • {TAGLINE}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None,
        )
        try:
            await interaction.edit_original_response(embed=follow_up_embed, view=None)
            await asyncio.sleep(10)
            await interaction.delete_original_response()
        except discord.NotFound:
            pass


async def setup(bot):
    await bot.add_cog(GenerateCog(bot))
