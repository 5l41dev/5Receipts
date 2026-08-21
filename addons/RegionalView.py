# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import json
import sqlite3
from datetime import datetime

import discord
from discord import ui

from addons.settings import SettingsView
from modals.acnestudios import acnemodal
from modals.adidas import adidasmodal
from modals.amazon import amazonmodal
from modals.arcteryx import arcteryxmodal
from modals.brokenplanet import brokenmodal
from modals.burberry import burberrymodal
from modals.cartier import cartiermodal
from modals.chanel import chanelmodal
from modals.chewforever import Chewforevermodal
from modals.chromehearts import chromemodal
from modals.chrono import chronomodal
from modals.coolblue import coolbluemodal
from modals.culturekings import ckmodal
from modals.denimtears import denimtearsmodal
from modals.dior import diormodal
from modals.dyson import dyson
from modals.apple import applemodal
from modals.balenciaga import balenciagamodal
from modals.bape import bapemodal
from modals.canadagoose import canadagoose
from modals.ebayauth import ebayauthmodal
from modals.end import endmodal
from modals.flannels import flannelsmodal
from modals.gallerydept import gallerydeptmodal
from modals.goat import goat
from modals.grailed import grailedmodal
from modals.jdsports import jdsportsmodal
from modals.legitapp import legitappmodal
from modals.loropiana import loromodal
from modals.maisonmargiela import maisonmodal
from modals.moncler import monclermodal
from modals.nike import nikemodal
from modals.nosauce import nosaucemodal
from modals.pandora import pandoramodal
from modals.prada import Pradamodal
from modals.ralphlauren import ralphlaurenmodal
from modals.sephora import sephoranmodal
from modals.snkrs import snkrsmodal
from modals.spider import spidermodal
from modals.stockx import stockxmodal
from modals.lv import lvmodal
from modals.crtz import crtzmodal
from modals.farfetch import farfetchmodal
from modals.breuninger import breuningermodal
from modals.stussy import stussymodal
from modals.tnf import tnfmodal
from modals.trapstar import trapstarmodal
from modals.zalandode import zalandodemodal
from modals.zalandous import zalandomodal
from modals.zara import zaramodal
from modals.fightclub import fightclubmodal
from utils.theme import BRAND, PURPLE, TAGLINE

conn = sqlite3.connect("data.db")
cursor = conn.cursor()


def get_bot_name(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("bot_name", BRAND)
    except (FileNotFoundError, json.JSONDecodeError):
        return BRAND


def get_client_id(config_path="config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        raw = config.get("client_role_id", "")
        return int(raw) if str(raw).isdigit() else 0


clientid = get_client_id()


brands = {
    "USA": {
        "Acne Studios": acnemodal,
        "Adidas": adidasmodal,
        "Amazon": amazonmodal,
        "Arc’teryx": arcteryxmodal,
        "Broken Planet": brokenmodal,
        "Burberry": burberrymodal,
        "Cartier": cartiermodal,
        "Chanel": chanelmodal,
        "Chew Forever": Chewforevermodal,
        "Chrome Hearts": chromemodal,
        "Chrono24": chronomodal,
        "Coolblue": coolbluemodal,
        "Culture Kings": ckmodal,
        "Denim Tears": denimtearsmodal,
        "Dior": diormodal,
        "Dyson": dyson,
        "Apple": applemodal,
        "Balenciaga": balenciagamodal,
        "Bape": bapemodal,
        "Canada Goose": canadagoose,
        "END.": endmodal,
        "Flannels": flannelsmodal,
        "Gallery Dept": gallerydeptmodal,
        "Goat": goat,
        "JD Sports": jdsportsmodal,
        "Loro Piana": loromodal,
        "Maison Margiela": maisonmodal,
        "Moncler": monclermodal,
        "Nike": nikemodal,
        "No Sauce The Plug": nosaucemodal,
        "Pandora": pandoramodal,
        "Prada": Pradamodal,
        "Ralph Lauren": ralphlaurenmodal,
        "Sephora": sephoranmodal,
        "Spider": spidermodal,
        "StockX": stockxmodal,
        "Louis Vuitton": lvmodal,
        "Corteiz": crtzmodal,
        "Farfetch": farfetchmodal,
        "Stüssy": stussymodal,
        "The North Face": tnfmodal,
        "Trapstar": trapstarmodal,
        "Zalando US": zalandomodal,
        "Flight Club": fightclubmodal,
        "Grailed": grailedmodal,
    },
    "DE": {
        "Breuninger": breuningermodal,
        "Zalando DE": zalandodemodal,
        "Zara": zaramodal,
    },
    "AUTH": {
        "Snkrs": snkrsmodal,
        "Legit App": legitappmodal,
        "Ebay": ebayauthmodal,
    },
}


def load_brands(region="USA"):
    return sorted(brands[region].items(), key=lambda x: x[0])


brands_auth = load_brands("AUTH")
brands_usa = load_brands("USA")
brands_de = load_brands("DE")


def dashboard_embed(user=None):
    """Shared dashboard embed shown when a user goes back to region selection."""
    embed = discord.Embed(
        title="💜 Dashboard",
        description="🔒 No access found — grab a plan to start cooking.",
        color=PURPLE,
    )
    cursor.execute("SELECT expiry, key FROM licenses WHERE owner_id = ?", (str(user.id),) if user else ("",))
    x = cursor.fetchone()
    if x:
        expiry_str, key = x
        extime = datetime.strptime(expiry_str, "%d/%m/%Y %H:%M:%S")
        now = datetime.now()
        delta = extime - now
        days_left = delta.days
        hours_left = delta.total_seconds() // 3600

        if extime < now:
            embed.description = "❌ Your plan expired — renew to keep cooking."
        elif key.startswith("LifetimeKey"):
            embed.description = "🌍 Pick a region below. You're on **``Lifetime``** — enjoy! ✨"
        elif days_left > 0:
            embed.description = (
                "🌍 Pick a region below.\n"
                f"You have **``{days_left} Days``** left on your plan. ⏳"
            )
        else:
            embed.description = (
                "🌍 Pick a region below.\n"
                f"You have **``{int(hours_left)} Hours``** left on your plan. ⏳"
            )
        if user:
            embed.set_footer(
                text=f"{user}'s Panel • {TAGLINE}",
                icon_url=user.avatar.url if user.avatar else None,
            )
    return embed


class PaginatedDropdown(discord.ui.Select):
    def __init__(self, owner_id, options, per_page=25):
        super().__init__(placeholder="Select a brand to proceed", min_values=1, max_values=1)
        self.owner_id = owner_id
        self.all_options = options
        self.per_page = per_page
        self.page = 0
        self.update_options(self.page)

    def update_options(self, page):
        self.page = page
        start = self.page * self.per_page
        end = start + self.per_page
        self.options = [
            discord.SelectOption(label=name, value=name)
            for name, _ in self.all_options[start:end]
        ]

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )
            return

        selected_brand = self.values[0]
        modal_function = dict(self.all_options).get(selected_brand)
        if callable(modal_function):
            await interaction.response.send_modal(modal_function())
        else:
            await interaction.response.send_message(
                "Hmm, that modal isn't wired up yet — try another brand.", ephemeral=True
            )


class DropdownView(discord.ui.View):
    def __init__(self, owner_id, options, per_page=13):
        super().__init__()
        self.owner_id = owner_id
        self.dropdown = PaginatedDropdown(owner_id, sorted(options), per_page)
        self.add_item(self.dropdown)
        region = "US"
        self.region = region

        if options == brands_de:
            self.region = "DE"
            self.next_button.disabled = True
            self.previous_button.disabled = True
        elif options == brands_usa:
            self.region = "US"
        elif options == brands_auth:
            self.region = "AUTH"

    def update_footer(self, interaction: discord.Interaction):
        bot_name = get_bot_name()
        footer_text = f"Page {self.dropdown.page + 1} of {self.calculate_total_pages()}"
        embed = discord.Embed(
            title=bot_name,
            description=(
                f"Pick a brand to start cooking.\n"
                f"You have access to `all` {self.region} receipts."
            ),
            color=PURPLE,
        )
        embed.set_footer(text=footer_text, icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        return embed

    def calculate_total_pages(self):
        return (len(self.dropdown.all_options) + self.dropdown.per_page - 1) // self.dropdown.per_page

    def update_buttons(self):
        total_pages = self.calculate_total_pages()
        self.previous_button.disabled = self.dropdown.page == 0
        self.next_button.disabled = self.dropdown.page >= total_pages - 1

    async def update_buttons_and_footer(self, interaction: discord.Interaction):
        self.update_buttons()
        embed = self.update_footer(interaction)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.grey, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            if self.dropdown.page > 0:
                self.dropdown.update_options(self.dropdown.page - 1)
                await self.update_buttons_and_footer(interaction)
        else:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button, disabled=False):
        if interaction.user.id == self.owner_id:
            total_pages = self.calculate_total_pages()
            if self.dropdown.page < total_pages - 1:
                self.dropdown.update_options(self.dropdown.page + 1)
                await self.update_buttons_and_footer(interaction)
        else:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

    @discord.ui.button(label="Go Back")
    async def handle_leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            embed = dashboard_embed(interaction.user)
            region_view = RegionSelectionView(interaction.user.id, interaction.user.roles)
            await interaction.response.edit_message(embed=embed, view=region_view)
        else:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )


class RegionSelectionView(discord.ui.View):
    def __init__(self, owner_id, user_roles):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.user_roles = user_roles

    def _has_valid_license(self, interaction):
        cursor.execute(
            "SELECT key, expiry, emailtf, credentialstf FROM licenses WHERE owner_id = ?",
            (str(interaction.user.id),),
        )
        return cursor.fetchone()

    async def _gate_region(self, interaction, region):
        license_data = self._has_valid_license(interaction)
        if not license_data:
            embed = discord.Embed(
                title="💜 Dashboard",
                description="🚫 No valid plan found for your account.",
                color=PURPLE,
            )
            return await interaction.response.edit_message(embed=embed)

        key, expiry_str, emailtf, credentialstf = license_data
        extime = datetime.strptime(expiry_str, "%d/%m/%Y %H:%M:%S")
        now = datetime.now()

        if extime <= now:
            embed = discord.Embed(
                title="💜 Dashboard",
                description="❌ Your plan expired — renew to keep cooking.",
                color=PURPLE,
            )
            return await interaction.response.edit_message(embed=embed)

        if emailtf != "True" or credentialstf != "True":
            missing = []
            if emailtf != "True":
                missing.append("an **email**")
            if credentialstf != "True":
                missing.append("your **credentials**")
            embed = discord.Embed(
                title="💜 Dashboard",
                description=(
                    f"Almost there! Head to **Settings** and set up {', '.join(missing)} "
                    "before generating."
                ),
                color=PURPLE,
            )
            embed.set_footer(
                text=f"{interaction.user}'s Panel • {TAGLINE}",
                icon_url=interaction.user.avatar.url if interaction.user.avatar else None,
            )
            return await interaction.response.edit_message(embed=embed)

        await self.show_brand_selection(interaction, region)

    @discord.ui.button(label="English")
    async def usa_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            await self._gate_region(interaction, "USA")
        else:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

    @discord.ui.button(label="German")
    async def de_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            await self._gate_region(interaction, "DE")
        else:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

    @discord.ui.button(label="Auth")
    async def auth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            await self._gate_region(interaction, "AUTH")
        else:
            await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

    @discord.ui.button(label="Settings")
    async def settings_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message(
                content="This isn't your session — back off! 😤", ephemeral=True
            )

        cursor.execute(
            "SELECT key, expiry, emailtf, credentialstf FROM licenses WHERE owner_id = ?",
            (str(interaction.user.id),),
        )
        license_data = cursor.fetchone()

        if not license_data:
            embed = discord.Embed(
                title="💜 Dashboard",
                description="🚫 No valid plan found for your account.",
                color=PURPLE,
            )
            return await interaction.response.edit_message(embed=embed)

        key, expiry_str, emailtf, credentialstf = license_data
        extime = datetime.strptime(expiry_str, "%d/%m/%Y %H:%M:%S")
        now = datetime.now()

        if extime < now:
            embed = discord.Embed(
                title="💜 Dashboard",
                description="❌ Your plan expired — renew to keep cooking.",
                color=PURPLE,
            )
            view = None
        else:
            embed = discord.Embed(
                title="💜 Dashboard",
                description=(
                    f"Here's where your setup stands — fill in anything missing.\n\n"
                    f"📧 Email = **{emailtf}**\n"
                    f"👤 Credentials = **{credentialstf}**"
                ),
                color=PURPLE,
            )
            view = SettingsView(self.owner_id, interaction.user.roles)
            embed.set_footer(
                text=f"{interaction.user}'s Panel • {TAGLINE}",
                icon_url=interaction.user.avatar.url if interaction.user.avatar else None,
            )

        await interaction.response.edit_message(embed=embed, view=view)

    async def show_brand_selection(self, interaction, region):
        bot_name = get_bot_name()
        owner_id = interaction.user.id
        user_roles = interaction.user.roles
        user_roles_ids = [role.id for role in interaction.user.roles]

        embed = None
        view = None

        is_vip = clientid == 0 or clientid in user_roles_ids

        if region == "DE":
            if is_vip:
                embed = discord.Embed(
                    title=bot_name,
                    description="Pick a brand to start cooking.\nYou have access to `all` DE receipts.",
                    color=PURPLE,
                )
                view = DropdownView(owner_id, brands_de)
            else:
                embed = discord.Embed(
                    title=bot_name,
                    description="🔒 No access to DE receipts yet — grab a plan first.",
                    color=PURPLE,
                )
                view = RegionSelectionView(owner_id, user_roles)
        elif region == "USA":
            if is_vip:
                embed = discord.Embed(
                    title=bot_name,
                    description="Pick a brand to start cooking.\nYou have access to `all` US receipts.",
                    color=PURPLE,
                )
                view = DropdownView(owner_id, brands_usa)
            else:
                embed = discord.Embed(
                    title=bot_name,
                    description="🔒 No access to US receipts yet — grab a plan first.",
                    color=PURPLE,
                )
                view = RegionSelectionView(owner_id, user_roles)
        elif region == "AUTH":
            if is_vip:
                embed = discord.Embed(
                    title=bot_name,
                    description="Pick a brand to start authenticating.\nYou have access to `all` AUTH receipts.",
                    color=PURPLE,
                )
                view = DropdownView(owner_id, brands_auth)
            else:
                embed = discord.Embed(
                    title=bot_name,
                    description="🔒 No access to AUTH receipts yet — grab a plan first.",
                    color=PURPLE,
                )
                view = RegionSelectionView(owner_id, user_roles)

        if embed is None:
            embed = discord.Embed(
                title=bot_name,
                description="Something went wrong — try again in a bit.",
                color=PURPLE,
            )
            view = None

        embed.set_footer(
            text=f"{interaction.user}'s Panel • {TAGLINE}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None,
        )

        await interaction.response.edit_message(embed=embed, view=view)
