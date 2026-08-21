# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import asyncio
from base64 import b64decode
import json
import random
import re
import webbrowser
import discord
from discord.ui import Select
from discord import SelectOption, ui, app_commands
from datetime import datetime

import hashlib
import sys

import os
import json as jsond  # json
import time  # sleep before exit
import binascii  # hex encoding
from uuid import uuid4

import requests  # gen random guid



import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


from bs4 import BeautifulSoup
from pystyle import Colors
from utils.theme import PURPLE, CREDIT


r = Colors.red
lg = Colors.light_gray





class ebayauthmodal(ui.Modal, title="5Receipts"):
    pname = discord.ui.TextInput(label="Product Name", placeholder="Product Name", required=True)
    imageurl = discord.ui.TextInput(label="Image URL (Discord Image)", placeholder="https://cdn.discordapp.com/attachments/...", required=True)
    price = discord.ui.TextInput(label="Price without currency", placeholder="100.00", required=True)
    tax = discord.ui.TextInput(label="Shipping without currency", placeholder="10.00", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)





    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            pname = self.pname.value
            imageurl = self.imageurl.value
            price = self.price.value
            tax = self.tax.value
            currency = self.currency.value


            
            try:


                embed = discord.Embed(title="⚙️ Cooking Your Receipt...", description="Your receipt is being cooked — it'll hit your inbox any second! 💜", color=PURPLE)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


                with open("receipt/ebayauth.html", "r", encoding="utf-8") as file:
                    html_content = file.read()



                html_content = html_content.replace("{imageurl}", imageurl)
                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{pname}", pname)
                html_content = html_content.replace("{currency}", currency)
                html_content = html_content.replace("{price}", price)
                html_content = html_content.replace("{shipping}", tax)













                with open("receipt/updatedrecipies/updatedebayauth.html", "w", encoding="utf-8") as file:
                    file.write(html_content)



                sender_email = "eBay <authentication@ebay.shop>"
                subject = f"Your item has been authenticated!"

                from emails.choise import choiseView
                owner_id = interaction.user.id
                link = "https://ebay.com"
                pname = "AUTHENTICATED"


                    
                embed = discord.Embed(title="📮 Choose Delivery Method", description="Your receipt is ready — pick how you want it delivered.", color=PURPLE)
                embed.set_footer(text=CREDIT)
                view = choiseView(owner_id, html_content, sender_email, subject, pname, imageurl, link)
                await interaction.edit_original_response(embed=embed, view=view)
            except Exception as e:
                embed = discord.Embed(title="🚫 Something Went Wrong", description=f"An error occurred: {str(e)}", color=PURPLE)
                await interaction.edit_original_response(embed=embed)


        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="🚫 Something Went Wrong", description="No user details on file — set up your info in Settings first.", color=PURPLE)
            await interaction.response.send_message(embed=embed, ephemeral=True)

