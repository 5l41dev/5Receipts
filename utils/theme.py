# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
"""
Central theme for the bot.

Change PURPLE below once and every embed across the bot updates.
Change DEVELOPER / DEV_URL once and every credit across the bot updates.
"""

# The signature purple used on every embed
PURPLE = 0xA855F7

# Bot / brand name shown in modals, footers and embeds
BRAND = "5Receipts"

# Developer credit — swap these for your own handle/link
DEVELOPER = "5l41"
DEV_URL = "https://5l41.nex4.xyz"
CREDIT = f"Developed by {DEVELOPER} • {DEV_URL}"

# Small footer tagline used across panels (carries the dev credit everywhere)
TAGLINE = f"Cooked to order • Developed by {DEVELOPER}"

# Fallback brand used if config.json is missing or empty
FALLBACK_NAME = "5Receipts"


def brand_name(config_path="config.json"):
    """Return the configured bot name, falling back to BRAND."""
    try:
        import json

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("bot_name", BRAND)
    except (FileNotFoundError, json.JSONDecodeError):
        return BRAND


def embed(**kwargs):
    """Shortcut that always paints embeds purple."""
    import discord

    kwargs.setdefault("color", PURPLE)
    return discord.Embed(**kwargs)
