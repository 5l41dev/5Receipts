# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import discord
from discord.ext import commands

from addons.paypalbuttons import paypalView
from utils.config import PAYPAL_EMAIL, PAYPAL_PING_ROLE_ID, role_mention
from utils.theme import PURPLE, TAGLINE


class paypalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="paypal", description="Displays the payment address for a plan")
    @discord.app_commands.choices(
        amount=[
            discord.app_commands.Choice(name="14.99€ - Month", value="14.99€"),
            discord.app_commands.Choice(name="29.99€ - Lifetime", value="29.99€"),
            discord.app_commands.Choice(name="Custom Input", value="custominput"),
        ]
    )
    async def paypal(self, interaction: discord.Interaction, amount: str, custom: str = None):
        if amount == "custominput":
            if custom is None:
                await interaction.response.send_message(
                    "Please provide a custom amount with the `custom` option.", ephemeral=True
                )
                return
            amount = custom

        if not PAYPAL_EMAIL:
            return await interaction.response.send_message(
                "The owner hasn't set a PayPal email in `config.json` yet.", ephemeral=True
            )

        embed = discord.Embed(
            title="💜 Payment Time",
            description="Can you send via **Friends & Family**? Tap a button below.",
            color=PURPLE,
        )
        embed.set_footer(text=TAGLINE)

        ping = role_mention(PAYPAL_PING_ROLE_ID)
        content = f"{ping} {interaction.user.mention}" if ping else interaction.user.mention
        view = paypalView(PAYPAL_EMAIL, amount)
        await interaction.response.send_message(content=content, embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(paypalCog(bot))
