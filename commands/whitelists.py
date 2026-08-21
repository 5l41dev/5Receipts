# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import json

import discord
from discord.ext import commands

from utils.theme import PURPLE, TAGLINE
from utils.utils import Utils

config = json.load(open("config.json", encoding="utf-8"))


class whitelistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _denied_embed(self):
        return discord.Embed(
            title="🚫 Not Whitelisted",
            description="You're not allowed to use this panel — reach out to the owner.",
            color=PURPLE,
        )

    def _owner_embed(self):
        return discord.Embed(
            title="👑 Already Owner",
            description="That's the bot owner — they're always whitelisted, no need to touch them.",
            color=PURPLE,
        )

    @discord.app_commands.command(name="whitelist", description="Grant a user staff access")
    @discord.app_commands.describe(value="Member to whitelist")
    async def whitelist(self, interaction: discord.Interaction, value: discord.Member):
        whitelisted = await Utils.is_whitelisted(interaction.user.id)
        if not whitelisted:
            return await interaction.response.send_message(embed=self._denied_embed())

        if str(value.id) == config.get("owner_id", ""):
            return await interaction.response.send_message(embed=self._owner_embed())

        if await Utils.add_to_whitelist(value.id):
            embed = discord.Embed(
                title="✅ Whitelisted",
                description=f"{value.mention} can now use staff commands.",
                color=PURPLE,
            )
        else:
            embed = discord.Embed(
                title="🤔 Already Whitelisted",
                description=f"{value.mention} is already on the staff list.",
                color=PURPLE,
            )
        embed.set_footer(text=TAGLINE)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="unwhitelist", description="Revoke a user's staff access")
    @discord.app_commands.describe(value="Member to unwhitelist")
    async def unwhitelist(self, interaction: discord.Interaction, value: discord.Member):
        whitelisted = await Utils.is_whitelisted(interaction.user.id)
        if not whitelisted:
            return await interaction.response.send_message(embed=self._denied_embed())

        if str(value.id) == config.get("owner_id", ""):
            return await interaction.response.send_message(embed=self._owner_embed())

        if await Utils.remove_from_whitelist(value.id):
            embed = discord.Embed(
                title="✅ Unwhitelisted",
                description=f"Staff access revoked for {value.mention}.",
                color=PURPLE,
            )
        else:
            embed = discord.Embed(
                title="🤔 Not Whitelisted",
                description=f"{value.mention} wasn't on the staff list anyway.",
                color=PURPLE,
            )
        embed.set_footer(text=TAGLINE)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(whitelistCog(bot))
