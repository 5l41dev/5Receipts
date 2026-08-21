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
from utils.config import ZYTE_KEY


r = Colors.red
lg = Colors.light_gray





def is_goat_link(link):
    goat_link_pattern = re.compile(r'^https?://(www\.)?goat\.com/.*$')
    return bool(goat_link_pattern.match(link))


class goat(ui.Modal, title="5Receipts"):
    Link = discord.ui.TextInput(label="Link", placeholder="Goat link", required=True)
    currency = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    colorr = discord.ui.TextInput(label="Color", placeholder="Black", required=True)
    sizee = discord.ui.TextInput(label="Size (If no size leave blank)", placeholder="US M", required=False)
    price = discord.ui.TextInput(label="Price without Currency", placeholder="1693", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            link = self.Link.value
            currency = self.currency.value
            colorr = self.colorr.value
            sizee = self.sizee.value if self.sizee.value else ""
            

            if not is_goat_link(link):
                embed = discord.Embed(title="Error - Invalid Goat link", description="Please provide a valid Goat link.", color=PURPLE)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return


            
            try:


                embed = discord.Embed(title="⚙️ Cooking Your Receipt...", description="Your receipt is being cooked — it'll hit your inbox any second! 💜", color=PURPLE)
                await interaction.response.send_message(content=f"{interaction.user.mention}", embed=embed)


                with open("receipt/goat.html", "r", encoding="utf-8") as file:
                    html_content = file.read()


                # Zyte API setup
                url = link  # Link should be defined or passed into the class

                # Try Zyte API request
                try:
                    api_response = requests.post(
                        "https://api.zyte.com/v1/extract",
                        auth=(ZYTE_KEY, ""),
                        json={
                            "url": url,
                            "browserHtml": True,
                            "product": True,
                            "productOptions": {"extractFrom": "browserHtml"},
                        },
                    )

                    if api_response.status_code == 401:
                        raise Exception("API key invalid or expired - falling back to manual input")

                    if api_response.status_code != 200:
                        raise Exception(f"API request failed with status {api_response.status_code}")

                    # Decode HTML data and parse it
                    response_json = api_response.json()
                    browser_html = response_json.get("browserHtml")
                    if browser_html is None:
                        raise Exception("Browser HTML not found in API response")

                    soup = BeautifulSoup(browser_html, 'html.parser')
                    print()
                    print(f"[{Colors.green}START Scraping{lg}] GOAT -> {interaction.user.id} ({interaction.user})" + lg)


                    og_image_url = "Image URL not found"

                    product_name = "Product Name not found"

                    # Check for additional product information in API response
                    product_data = response_json.get("product")
                    if product_data:
                        product_name = product_data.get("name") or product_name  # Override if name found and not None
                        main_image = product_data.get("mainImage")
                        if main_image:
                            og_image_url = main_image.get("url") or og_image_url  # Override if mainImage URL found and not None


                    print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)
                    print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {og_image_url}" + lg)



                    print(f"[{Colors.green}Scraping DONE{lg}] GOAT -> {interaction.user.id}" + lg)
                    print()

                except Exception as api_error:
                    print(f"API failed: {api_error} - Falling back to manual input")
                    # Fallback to manual input
                    product_name = "Product Name not found - Please enter manually"
                    og_image_url = "Image URL not found - Please enter manually"
                    print()
                    print(f"[{Colors.yellow}FALLBACK{lg}] GOAT -> {interaction.user.id} ({interaction.user})" + lg)
                    print(f"    [{Colors.cyan}Manual Input Required{lg}] Product Name: {product_name}" + lg)
                    print(f"    [{Colors.cyan}Manual Input Required{lg}] Image URL: {og_image_url}" + lg)
                    print()



                price = self.price.value



                html_content = html_content.replace("{imageurl}", og_image_url)
                html_content = html_content.replace("{pname}", product_name)
                html_content = html_content.replace("{sizee}", sizee)
                html_content = html_content.replace("{color}", colorr)
                html_content = html_content.replace("{price}", price)
                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{city}", city)
                html_content = html_content.replace("{zip}", zipp)
                html_content = html_content.replace("{country}", country)
                html_content = html_content.replace("{currency}", currency)





                with open("receipt/updatedrecipies/updatedgoat.html", "w", encoding="utf-8") as file:
                    file.write(html_content)


                sender_email = "GOAT <info@goat.com>"
                subject = f"Your GOAT order #511637332"

                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="📮 Choose Delivery Method", description="Your receipt is ready — pick how you want it delivered.", color=PURPLE)
                embed.set_footer(text=CREDIT)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, og_image_url, link)
                await interaction.edit_original_response(embed=embed, view=view)
            except Exception as e:
                embed = discord.Embed(title="🚫 Something Went Wrong", description=f"An error occurred: {str(e)}", color=PURPLE)
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="🚫 Something Went Wrong", description="No user details on file — set up your info in Settings first.", color=PURPLE)
            await interaction.response.send_message(embed=embed, ephemeral=True)



        