# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import os
import aiohttp
import discord
import json
from discord import ui
from datetime import datetime, timedelta

from utils.theme import PURPLE, TAGLINE, BRAND



def activity_name(config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("activity", "Serving fresh receipts")
    except FileNotFoundError:
        return "Serving fresh receipts"
    


class botnamemodal(ui.Modal, title="Bot Name"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    botname = ui.TextInput(label=" Bot Name ", style=discord.TextStyle.short, placeholder=BRAND, required=True)


    async def on_submit(self, interaction: discord.Interaction):
        botname = self.botname.value
        await self.bot.user.edit(username=botname)
        embed = discord.Embed(title="✅ Bot Name Updated", description=f"The bot is now called `{botname}`", color=PURPLE)
        embed.add_field(name="", value="Discord throttles renames — wait `15min` before changing it again!")
        embed.set_footer(text=TAGLINE)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        

class interfacenamemodal(ui.Modal, title="Interface Name"):
    interfacename = ui.TextInput(label=" Interface Name ", style=discord.TextStyle.short, placeholder=BRAND, required=True)


    async def on_submit(self, interaction: discord.Interaction):
        interfacename = self.interfacename.value
        
        config_path = "config.json"
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        config["bot_name"] = interfacename
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        with open(config_path, "r") as f:
            config = json.load(f)

        embed = discord.Embed(
            title="✅ Interface Name Updated",
            description=f"The interface is now called `{interfacename}`",
            color=PURPLE
        )
        embed.add_field(
            name="",
            value="Discord throttles renames — wait `15min` before changing it again!"
        )
        embed.set_footer(text=TAGLINE)
        await interaction.response.send_message(embed=embed, ephemeral=True)



class activitynamemodal(ui.Modal, title="Activity Name"):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    activityname = ui.TextInput(label=" Activity Name ", style=discord.TextStyle.short, placeholder="Serving fresh receipts", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        activity = self.activityname.value
        global activity1
        config_path = "config.json"
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        config["activity"] = activity
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        with open(config_path, "r") as f:
            config = json.load(f)


        await self.bot.change_presence(activity=discord.Game(name=activity))
        embed = discord.Embed(title="✅ Activity Updated", description=f"The bot now shows `{activity}`", color=PURPLE)
        embed.set_footer(text=TAGLINE)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        activity1 = activity_name()



class avatarmodal(ui.Modal, title="Avatar"):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    avatarurl = ui.TextInput(label=" Avatar URL ", style= discord.TextStyle.short, placeholder="https://....", required= True)


    async def on_submit(self, interaction: discord.Interaction):
        url = self.avatarurl.value
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                avatar_bytes = await resp.read()
        await self.bot.user.edit(avatar=avatar_bytes)

        embed = discord.Embed(title="✅ Avatar Updated", description=f"New look locked in — **{url}**", color=PURPLE)
        embed.add_field(name="", value="Discord throttles changes — wait `15min` before changing it again!")
        embed.set_footer(text=TAGLINE)
        await interaction.response.send_message(embed=embed, ephemeral=True)









class clientmodal(ui.Modal, title="Customer Role ID"):

    clientid = ui.TextInput(label=" Customer Role ID ", style=discord.TextStyle.short, placeholder="123456789012345678", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        clientid = self.clientid.value

        config_path = "config.json"
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}

        config["client_role_id"] = clientid
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        with open(config_path, "r") as f:
            config = json.load(f)

        embed = discord.Embed(title="✅ Customer Role Updated", description=f"Customer role set to <@&{clientid}>", color=PURPLE)
        embed.set_footer(text=TAGLINE)
        await interaction.response.send_message(embed=embed, ephemeral=True)



class botsettingsView(discord.ui.View):
    def __init__(self, owner_id, bot):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.bot = bot




    @discord.ui.button(label="Bot Name", emoji="ℹ️")
    async def handle_botname(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            bot = self.bot
            await interaction.response.send_modal(botnamemodal(self.bot))
        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)


    @discord.ui.button(label="Interface Name", emoji="ℹ️")
    async def handle_intname(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            bot = self.bot
            await interaction.response.send_modal(interfacenamemodal())
        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)

    @discord.ui.button(label="Actvity", emoji="ℹ️")
    async def handle_act(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            bot = self.bot
            await interaction.response.send_modal(activitynamemodal(self.bot))
        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)

    @discord.ui.button(label="Avatar", emoji="ℹ️")
    async def handle_avatar(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            bot = self.bot
            await interaction.response.send_modal(avatarmodal(self.bot))
        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)

    @discord.ui.button(label="Customer Role ID", emoji="ℹ️")
    async def handle_access(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.owner_id:
            bot = self.bot
            await interaction.response.send_modal(clientmodal())
        else:
            await interaction.response.send_message(content="This is not your Panel", ephemeral=True)






    