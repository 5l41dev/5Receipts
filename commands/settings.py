# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import discord
from discord.ext import commands

from addons.botsettings import botsettingsView
from utils.theme import PURPLE, TAGLINE
from utils.utils import Utils


class settingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="settings", description="Admin: tweak the bot's look & behavior")
    async def settings(self, interaction: discord.Interaction):
        whitelisted = await Utils.is_whitelisted(interaction.user.id)
        if not whitelisted:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="🚫 Not Whitelisted",
                    description="You're not allowed to use this panel — reach out to the owner.",
                    color=PURPLE,
                )
            )

        embed = discord.Embed(
            title="⚙️ Bot Settings",
            description="Pick an option below to change how the bot looks and behaves.",
            color=PURPLE,
        )
        embed.set_footer(text=TAGLINE)

        view = botsettingsView(interaction.user.id, self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(settingsCog(bot))
