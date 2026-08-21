# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import random

import discord
from discord import ui

from utils.theme import PURPLE, TAGLINE


class paypalView(discord.ui.View):
    def __init__(self, email, amount):
        super().__init__(timeout=None)
        self.email = email
        self.amount = amount
        self.notes = [
            "Taxi", "Food", "Uber", "Groceries", "From Mom",
            "Gift", "Utilities", "Dinner", "Drinks",
            "Movie", "Concert", "Book", "Fitness", "Health",
            "Donation", "Course", "Travel", "Hotel", "Flight",
            "Car Rental", "Shopping", "Sports", "Equipment", "Festival",
            "Parking", "Pet Supplies", "Party Supplies", "Art Supplies",
            "Gardening", "Household", "Beauty Products", "Personal Care",
            "Electronics", "Software", "Games", "Music", "Apparel",
        ]

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary)
    async def handle_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        note = random.choice(self.notes)
        embed = discord.Embed(title="💜 Payment Details", color=PURPLE)
        embed.add_field(name="📧 Email:", value=f"```{self.email}```", inline=False)
        embed.add_field(name="💰 Amount:", value=f"```{self.amount}```", inline=False)
        embed.add_field(name="📝 Note:", value=f"```{note}```", inline=False)
        embed.add_field(
            name="⚠️ Disclaimer:",
            value="Send via **Friends & Family** and copy the **Note** exactly as shown.",
            inline=False,
        )
        embed.set_footer(text=TAGLINE)
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def handle_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💤 Payment Canceled",
            description="No worries — hit `/paypal` again when you're ready.",
            color=PURPLE,
        )
        await interaction.response.edit_message(embed=embed, view=None)
