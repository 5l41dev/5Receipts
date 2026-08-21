# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import discord
from discord.ext import commands

from utils.theme import PURPLE, TAGLINE, DEV_URL


class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="See every command the bot offers")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="💜 5Receipts — Command Menu",
            description=(
                "Everything you need to run the show, all in one place.\n"
                "Commands with 👑 are for whitelisted staff only."
            ),
            color=PURPLE,
        )
        embed.add_field(
            name="🛒 Customer Commands",
            value=(
                "➜ **/generate** — Start cooking a 1:1 receipt\n"
                "➜ **/paypal** — Grab the payment details for a plan"
            ),
            inline=False,
        )
        embed.add_field(
            name="👑 Staff Commands",
            value=(
                "➜ **/panel** *(/edit)* — Inspect & manage a user's access\n"
                "➜ **/whitelist** — Grant a user staff access\n"
                "➜ **/unwhitelist** — Revoke staff access\n"
                "➜ **/settings** — Tweak bot name, avatar, activity & roles"
            ),
            inline=False,
        )
        embed.add_field(
            name="🎫 Support",
            value="➜ **/ticket** — Drop the ticket panel into your support channel",
            inline=False,
        )
        embed.set_footer(text=f"{TAGLINE} • {DEV_URL}")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(helpCog(bot))
