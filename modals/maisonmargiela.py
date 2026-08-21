# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import asyncio
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

from emails.normal import SendNormal


r = Colors.red
lg = Colors.light_gray



class maisonmodal(ui.Modal, title="5Receipts"):
    pname = discord.ui.TextInput(label="Product Name", placeholder="Shoes", required=True)
    imageurl = discord.ui.TextInput(label="Image URL (Discord Image)", placeholder="https://cdn.discordapp.com/attachments/...", required=True)
    price = discord.ui.TextInput(label="Price without currency", placeholder="178.96", required=True)
    shipping = discord.ui.TextInput(label="Shipping Costs", placeholder="10.00", required=True)
    tax = discord.ui.TextInput(label="Tax Costs", placeholder="10.00", required=True)




    async def on_submit(self, interaction: discord.Interaction):
        global name, street, city, zipp, country, pname, imageurl, price, shipping, tax
        from addons.nextsteps import NextstepMargiela
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
            price = float(self.price.value)
            shipping = float(self.shipping.value)
            tax = float(self.tax.value)




            
            embed = discord.Embed(title="🧩 One Last Step!", description="One more quick form and your receipt is ready to send. 🧾", color=PURPLE)
            await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed, view=NextstepMargiela(owner_id))

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="🚫 Something Went Wrong", description="No user details on file — set up your info in Settings first.", color=PURPLE)
            await interaction.response.send_message(embed=embed, ephemeral=True)





class maisonmodal2(ui.Modal, title="Maison Margiela Receipt"):
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    color = discord.ui.TextInput(label="Color", placeholder="Black", required=True)
    size = discord.ui.TextInput(label="Size", placeholder="M", required=True)
    orderdate = discord.ui.TextInput(label="Order Date (DD/MM/YYYY)", placeholder="14/06/2024", required=True)
    deliverydate = discord.ui.TextInput(label="Delivery Date (DD/MM/YYYY)", placeholder="17/04/2024", required=True)






    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 
        global name, street, city, zipp, country, pname, imageurl, price, currency, color
        try:

            embed = discord.Embed(title="⚙️ Cooking Your Receipt...", description="Your receipt is being cooked — it'll hit your inbox any second! 💜", color=PURPLE)
            await interaction.response.edit_message(embed=embed, view=None)

            



            with open("receipt/maisonmargiela.html", "r", encoding="utf-8") as file:
                html_content = file.read()



            currency = self.currency.value
            color = self.color.value
            size = self.size.value
            orderdate = self.orderdate.value
            deliverydate = self.deliverydate.value




                

            fulltotal =  shipping + tax + price
            fulltotal = round(fulltotal, 2)

            def generate_order_number():
                return str(random.randint(1000000, 9999999))  # Generiert eine Zahl zwischen 10000000 und 99999999

            # Bestellnummer generieren
            order_number = generate_order_number()


            html_content = html_content.replace("{name}", name)
            html_content = html_content.replace("{street}", street)
            html_content = html_content.replace("{city}", city)
            html_content = html_content.replace("{zip}", zipp)
            html_content = html_content.replace("{country}", country)

            html_content = html_content.replace("{ordernuber}", order_number)
            html_content = html_content.replace("{pname}", pname)
            html_content = html_content.replace("{imageurl}", imageurl)
            html_content = html_content.replace("{price}", str(price))
            html_content = html_content.replace("{shipping}", str(shipping))
            html_content = html_content.replace("{tax}", str(tax))
            html_content = html_content.replace("{total}", str(fulltotal))
            html_content = html_content.replace("{currency}", currency)
            html_content = html_content.replace("{color}", color)
            html_content = html_content.replace("{size}", size)
            html_content = html_content.replace("{orderdate}", orderdate)
            html_content = html_content.replace("{deliverydate}", deliverydate)













            

            with open("receipt/updatedrecipies/updatedmaisonmargiela.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            from emails.choise import choiseView
            sender_email = "Maison Margiela Online Store <orders@maisonmargiela.org>"
            subject = f"Confirmation of Your Order"
            link = "https://loropiana.com/"

                
            embed = discord.Embed(title="📮 Choose Delivery Method", description="Your receipt is ready — pick how you want it delivered.", color=PURPLE)
            embed.set_footer(text=CREDIT)
            view = choiseView(owner_id, html_content, sender_email, subject, pname, imageurl, link)
            await interaction.edit_original_response(embed=embed, view=view)

        except Exception as e:
            embed = discord.Embed(title="🚫 Something Went Wrong", description=f"An error occurred: {str(e)}", color=PURPLE)
            await interaction.edit_original_response(embed=embed)