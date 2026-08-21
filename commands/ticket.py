# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import discord
from discord import ui
from discord.ext import commands

from utils.config import STAFF_ROLE_ID, TICKET_CATEGORY_ID, TICKET_PANEL_CHANNEL
from utils.theme import PURPLE, TAGLINE, DEV_URL


class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Buy", style=discord.ButtonStyle.primary, custom_id="ticket_buy")
    async def buy_callback(self, interaction: discord.Interaction, button: ui.Button):
        await self.create_ticket(interaction, "buy")

    @ui.button(label="Question", style=discord.ButtonStyle.secondary, custom_id="ticket_question")
    async def question_callback(self, interaction: discord.Interaction, button: ui.Button):
        await self.create_ticket(interaction, "question")

    @ui.button(label="Partner", style=discord.ButtonStyle.success, custom_id="ticket_partner")
    async def partner_callback(self, interaction: discord.Interaction, button: ui.Button):
        await self.create_ticket(interaction, "partner")

    @ui.button(label="Support", style=discord.ButtonStyle.danger, custom_id="ticket_support")
    async def support_callback(self, interaction: discord.Interaction, button: ui.Button):
        await self.create_ticket(interaction, "support")

    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str):
        guild = interaction.guild
        user = interaction.user

        category = None
        if TICKET_CATEGORY_ID.isdigit():
            category = guild.get_channel(int(TICKET_CATEGORY_ID))

        channel_name = f"{ticket_type}-{user.name.lower()}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        if STAFF_ROLE_ID.isdigit():
            staff_role = guild.get_role(int(STAFF_ROLE_ID))
            if staff_role:
                overwrites[staff_role] = discord.PermissionOverwrite(
                    read_messages=True, send_messages=True
                )

        channel = await guild.create_text_channel(
            channel_name, category=category, overwrites=overwrites
        )

        embed = discord.Embed(
            title=f"🎫 Ticket: {ticket_type.capitalize()}",
            description=f"Welcome {user.mention}! A staff member will be with you shortly.",
            color=PURPLE,
        )
        embed.set_footer(text=f"{TAGLINE} • {DEV_URL}")
        await channel.send(embed=embed)

        await interaction.response.send_message(
            f"Ticket created: {channel.mention}", ephemeral=True
        )


class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ticket", description="Send the ticket panel to the configured channel")
    async def ticket_command(self, interaction: discord.Interaction):
        if not TICKET_PANEL_CHANNEL.isdigit():
            return await interaction.response.send_message(
                "Set `ticket_panel_channel` in `config.json` first.", ephemeral=True
            )

        target_channel = self.bot.get_channel(int(TICKET_PANEL_CHANNEL))
        if not target_channel:
            await interaction.response.send_message(
                "Target channel not found — check the ID in `config.json`.", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🎫 Support Tickets",
            description="Need help or want to buy? Hit a button and a ticket opens instantly.",
            color=PURPLE,
        )
        embed.add_field(name="💳 Buy", value="Purchasing a plan", inline=True)
        embed.add_field(name="❓ Question", value="General questions", inline=True)
        embed.add_field(name="🤝 Partner", value="Partnership requests", inline=True)
        embed.add_field(name="🛠️ Support", value="Technical help", inline=True)
        embed.set_footer(text=f"{TAGLINE} • {DEV_URL}")

        view = TicketView()
        await target_channel.send(embed=embed, view=view)
        await interaction.response.send_message("Ticket panel sent!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(TicketCog(bot))
