# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import json

import discord
from discord.ext import commands

from utils.adminpanel import PanelView
from utils.theme import PURPLE, TAGLINE, DEV_URL
from utils.utils import Utils


class adminpanelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="panel", description="Admin: inspect or edit a user's access")
    @discord.app_commands.describe(user="User to inspect or edit")
    async def adminpanel(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer()
        owner_id = interaction.user.id

        config = json.load(open("config.json", encoding="utf-8"))
        if str(interaction.user.id) != config.get("owner_id", ""):
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    title="🚫 Access Denied",
                    description="This command is locked to the bot owner only.",
                    color=PURPLE,
                )
            )

        whitelisted = await Utils.is_whitelisted(interaction.user.id)
        if not whitelisted:
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    title="🚫 Not Whitelisted",
                    description="You're not allowed to use this panel — reach out to the owner.",
                    color=PURPLE,
                )
            )

        embed = discord.Embed(
            title=f"👑 Admin Panel — {user}",
            description="Select an option below to manage this user's access.",
            color=PURPLE,
        )
        embed.set_footer(text=f"{TAGLINE} • {DEV_URL}")

        view = PanelView(owner_id, user=user.id)
        await interaction.edit_original_response(embed=embed, view=view)

    @discord.app_commands.command(name="edit", description="Admin: inspect or edit a user's access")
    @discord.app_commands.describe(user="User to inspect or edit")
    async def edit_alias(self, interaction: discord.Interaction, user: discord.Member):
        await self.adminpanel.callback(interaction, user)


async def setup(bot):
    await bot.add_cog(adminpanelCog(bot))
