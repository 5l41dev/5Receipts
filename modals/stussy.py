# 5Receipts — Developed by 5l41 • https://5l41.nex4.xyz
import asyncio
import json
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





def is_stussy_link(link):
    stussy_pattern = re.compile(r'^https?://(www\.)?eu\.stussy\.com/.+')

    return bool(stussy_pattern.match(link))


class stussymodal(ui.Modal, title="5Receipts"):
    Linkff = discord.ui.TextInput(label="Link", placeholder="eu.stussy.com link", required=True)
    Priceff = discord.ui.TextInput(label="Price without currency", placeholder="Ex. 790", required=True)
    delivery = discord.ui.TextInput(label="Shipping Costs without currency", placeholder="Ex. 7.99", required=True)
    currencyff = discord.ui.TextInput(label="Currency ($, €, £)", placeholder="€", required=True, min_length=1, max_length=2)
    Size = discord.ui.TextInput(label="Size", placeholder="Ex. XL", required=True)


    async def on_submit(self, interaction: discord.Interaction):
        owner_id = interaction.user.id 

        import sqlite3
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, street, city, zipp, country FROM licenses WHERE owner_id = ?", (str(owner_id),))
        user_details = cursor.fetchone()

        if user_details:
            name, street, city, zipp, country = user_details

            Linkff = self.Linkff.value
            currencyff = self.currencyff.value
            Priceff = self.Priceff.value
            delivery = self.delivery.value

            if not is_stussy_link(Linkff):
                embed = discord.Embed(title="Error - Invalid Stussy link", description="Please provide a valid Stussy link.", color=PURPLE)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            try:
                embed = discord.Embed(title="⚙️ Cooking Your Receipt...", description="Your receipt is being cooked — it'll hit your inbox any second! 💜", color=PURPLE)
                await interaction.response.send_message(content=f"{interaction.user.mention}",embed=embed)



                with open("receipt/stussy.html", "r", encoding="utf-8") as file:
                    html_content = file.read()



                # Zyte API setup
                url = Linkff

                # Zyte API request
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

                if api_response.status_code != 200:
                    raise Exception(f"API request failed with status {api_response.status_code}")

                # Decode HTML data and parse it
                response_json = api_response.json()
                browser_html = response_json.get("browserHtml")
                if browser_html is None:
                    raise Exception("Browser HTML not found in API response")

                soup = BeautifulSoup(browser_html, 'html.parser')
                print()
                print(f"[{Colors.green}START Scraping{lg}] STÜSSY -> {interaction.user.id} ({interaction.user})" + lg)

                product_name = "Product Name not found"
                colour = "Color not found"
                image_url = "Image URL not found"

                # Check for additional product information in API response
                product_data = response_json.get("product")
                if product_data:
                    product_name = product_data.get("name") or product_name
                    # For color, might need to find in HTML
                    colour_element = soup.find('div', {'class': 'product__variant-color pt-20 text-gray-silver uppercase font-500'})
                    if colour_element:
                        colour = colour_element.text.strip()
                    else:
                        colour = "Color not found"

                    main_image = product_data.get("mainImage")
                    if main_image:
                        image_url = main_image.get("url") or image_url

                print(f"    [{Colors.cyan}Scraping{lg}] Product Name: {product_name}" + lg)
                print(f"    [{Colors.cyan}Scraping{lg}] Color: {colour}" + lg)
                print(f"    [{Colors.cyan}Scraping{lg}] Image URL: {image_url}" + lg)

                print(f"[{Colors.green}Scraping DONE{lg}] STÜSSY -> {interaction.user.id}" + lg)
                print()


                size = self.Size.value


                tax = 7.65 

                Priceff = float(Priceff)
                delivery = float(delivery)

                total = Priceff + delivery + tax

                total = round(total, 2)


                html_content = html_content.replace("{name}", name)
                html_content = html_content.replace("{street}", street)
                html_content = html_content.replace("{city}", city)
                html_content = html_content.replace("{zip}", zipp)
                html_content = html_content.replace("{country}", country)
                html_content = html_content.replace("{shipping}", str(delivery))

                html_content = html_content.replace("{price}", str(Priceff)) 

                html_content = html_content.replace("{imgsrc}", str(image_url))
                html_content = html_content.replace("{productname}", product_name)
                html_content = html_content.replace("{color}", colour)
                html_content = html_content.replace("{size}", size)
                html_content = html_content.replace("{lnik}", Linkff)




                html_content = html_content.replace("{currency}", str(currencyff)) 
                html_content = html_content.replace("{fulltotal}", str(total))
                

                with open("receipt/updatedrecipies/updatedstussy.html", "w", encoding="utf-8") as file:
                    file.write(html_content)

                sender_email = "Stussy <noreply@stussy.com>"
                subject = "Order #790837 confirmed"
                from emails.choise import choiseView
                owner_id = interaction.user.id

                    
                embed = discord.Embed(title="📮 Choose Delivery Method", description="Your receipt is ready — pick how you want it delivered.", color=PURPLE)
                embed.set_footer(text=CREDIT)
                view = choiseView(owner_id, html_content, sender_email, subject, product_name, image_url, Linkff)
                await interaction.edit_original_response(embed=embed, view=view)
                    
            except Exception as e:
                embed = discord.Embed(title="🚫 Something Went Wrong", description=f"An error occurred: {str(e)}", color=PURPLE)
                await interaction.edit_original_response(embed=embed)

        else:
            # Handle case where no user details are found
            embed = discord.Embed(title="🚫 Something Went Wrong", description="No user details on file — set up your info in Settings first.", color=PURPLE)
            await interaction.response.send_message(embed=embed, ephemeral=True)



    