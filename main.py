# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import os
import threading

import discord
from discord.ext import commands
from flask import Flask
from pystyle import Colors

from utils.config import (
    BOT_TOKEN,
    OWNER_ID,
    PIC_CHANNEL,
    channel_mention,
    config,
)
from utils.database import init_db

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# Only enforce the "post image -> get url" channel when one is configured
PIC_CHANNEL_ID = int(PIC_CHANNEL) if PIC_CHANNEL.isdigit() else None


async def load_cogs():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension(f"commands.{filename[:-3]}")


def activity_name():
    return config.get("activity", "Serving fresh receipts")


@bot.event
async def on_ready():
    # Fresh-clone safety: create the database schema, output folder + whitelist the owner.
    init_db()
    os.makedirs("receipt/updatedrecipies", exist_ok=True)
    try:
        with open("whitelist.txt", "r", encoding="utf-8") as f:
            whitelisted = f.read().splitlines()
        if OWNER_ID and OWNER_ID not in whitelisted:
            with open("whitelist.txt", "a", encoding="utf-8") as f:
                f.write(f"{OWNER_ID}\n")
            print(f"[Setup] Auto-whitelisted owner {OWNER_ID}")
    except FileNotFoundError:
        with open("whitelist.txt", "w", encoding="utf-8") as f:
            f.write(f"{OWNER_ID}\n")

    activity = discord.Activity(
        name=activity_name(),
        type=discord.ActivityType.competing,
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await load_cogs()
    await bot.tree.sync()

    print(f"\n\nLogged in as {bot.user} | In {len(bot.guilds)} servers:")
    for guild in bot.guilds:
        print(Colors.purple + guild.name + Colors.reset)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg_content = message.content.lower()
    setup = channel_mention(config.get("setup_guide_channel", ""))
    sales = channel_mention(config.get("sales_channel", ""))

    if "how" in msg_content and "generate" in msg_content:
        await message.reply(
            f"Fresh out the kitchen, huh? 🔮 Run `/generate`, pick a region, "
            f"grab your brand and cook. {setup}".strip()
        )
    elif ("difference" in msg_content or "diff" in msg_content) and "spoofed" in msg_content:
        await message.reply(
            "**Spoofed** sends from the brand's own domain (`noreply@stockx.com`) "
            "so it looks fully native. **Normal** sends from our domain instead. "
            "Both receipts are identical 1:1 — spoofed just hits harder. 💜"
        )
    elif "need" in msg_content and "pay" in msg_content:
        await message.reply(
            f"Nothing in life is free — not even receipts. 😌 Check the prices "
            f"and grab a plan to unlock the generator. {sales}".strip()
        )
    elif "it" in msg_content and "paid" in msg_content:
        await message.reply(
            f"Receipts aren't free, sorry! 😅 Check the prices and grab a plan "
            f"to unlock the generator. {sales}".strip()
        )
    elif "receive" in msg_content and "email" in msg_content:
        await message.reply(
            "No email in sight? Check your **spam folder** first — if it's there, "
            "move it to the inbox so the images load. Still nothing? Double-check "
            "the email you entered in Settings. 📬"
        )
    elif "/gen" in msg_content:
        await message.reply(
            f"Type `/generate` to start cooking 1:1 receipts! {setup}".strip()
        )

    if PIC_CHANNEL_ID is None or message.channel.id != PIC_CHANNEL_ID:
        await bot.process_commands(message)
        return

    for attachment in message.attachments:
        if any(
            attachment.filename.lower().endswith(ext)
            for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]
        ):
            await message.reply(f"```{attachment.url}```")
            return

    await bot.process_commands(message)


# Flask app for Render.com / Railway port binding
app = Flask(__name__)


@app.route("/")
def home():
    return "5Receipts is running! — Developed by 5l41 • https://5l41.nex4.xyz"


def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

bot.run(BOT_TOKEN)
