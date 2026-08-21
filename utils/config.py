# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
"""
Central config loader.

Every secret (bot token, SMTP, Zyte key) and every channel/role ID is read
from config.json through this module, so a fresh setup only has to fill in
config.json once.
"""

import json


def load_config(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


config = load_config()

# --- Secrets -----------------------------------------------------------------
BOT_TOKEN = config.get("tokens", {}).get("main", "")
ZYTE_KEY = config.get("zyte", {}).get("api_key", "")
SMTP = config.get("smtp", {})

# --- Owner -------------------------------------------------------------------
OWNER_ID = str(config.get("owner_id", ""))

# --- Roles (IDs) -------------------------------------------------------------
CLIENT_ROLE_ID = str(config.get("client_role_id", ""))
STAFF_ROLE_ID = str(config.get("staff_role_id", ""))
PAPER_ACCESS_ROLE_ID = str(config.get("paper_access_role_id", ""))
EMU_ACCESS_ROLE_ID = str(config.get("emu_access_role_id", ""))
PAYPAL_PING_ROLE_ID = str(config.get("paypal_ping_role_id", ""))

# --- Channels (IDs) ----------------------------------------------------------
PIC_CHANNEL = str(config.get("pic_channel", ""))
GENERAL_CHANNEL = str(config.get("general_channel", ""))
TICKET_CATEGORY_ID = str(config.get("ticket_category_id", ""))
TICKET_PANEL_CHANNEL = str(config.get("ticket_panel_channel", ""))
SETUP_GUIDE_CHANNEL = str(config.get("setup_guide_channel", ""))
VOUCH_CHANNEL = str(config.get("vouch_channel", ""))
SALES_CHANNEL = str(config.get("sales_channel", ""))

# --- Misc --------------------------------------------------------------------
PAYPAL_EMAIL = config.get("paypal_email", "")
INVITE = config.get("invite", "")


def channel_mention(channel_id: str) -> str:
    """Return a clickable <#id> mention, or '' when the ID is not configured."""
    if channel_id and channel_id.isdigit():
        return f"<#{channel_id}>"
    return ""


def role_mention(role_id: str) -> str:
    """Return a clickable <@&id> mention, or '' when the ID is not configured."""
    if role_id and role_id.isdigit():
        return f"<@&{role_id}>"
    return ""
