from json import load
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import scraper
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os

"""
Program should run webscraper upon using "/bestbuy" list all entries on
search page, and upon adding item to "cart" continuosly reload page every 
60 seconds or so and email upon restock 

Selection menu for which item to add to "cart"

"""

scraped = scraper.webscraping()
load_dotenv('.env')
TOKEN=os.getenv('TOKEN')
NoneType = type(None)

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix= '!', intents=intents)

testingServerID = 1011744383281942699

@client.slash_command(name = "hello", description="reply with hello", guild_ids=[testingServerID])
async def hello_command(interaction: Interaction):
    await interaction.response.send_message("Hello")

@client.event
async def on_message(message): 
    if message.author == client.user:
        return

    cor_message = message.content.lower()

    if f'$search' in cor_message: 
        keywords = scraped.get_keywords(cor_message)
        url = scraped.send_url(keywords)
        scraped.driver.get(url)
        #scrolling()
        #getting item names and urls
        items = scraped.driver.find_elements(By.CLASS_NAME, 'sku-title [href]')
        links = [item.get_attribute('href') for item in items]
        #getting statuses for stock
        statuses = scraped.driver.find_elements(By.CLASS_NAME, "fulfillment-fulfillment-summary")
        #get price 
        prices = scraped.driver.find_elements(By.CLASS_NAME, 'priceView-hero-price.priceView-customer-price')
        # "c-button c-button-disabled c-button-sm c-button-block add-to-cart-button"

        for i in range(4):
            s = str(prices[i].text) + ". Item is: " + str(statuses[i].text)+ "\n" + str(items[i].text)
            await message.channel.send(s)

        while (True):
            response = await client.wait_for('message')
            try: 
                ind = int(response.content)
                await message.channel.send(statuses[ind].text)
                if ("Get it in" not in statuses[ind].text):
                    await message.channel.send("Unavailable or sold out atm. Message will be sent upon restock")
                while ("Get it in" not in statuses[ind].text):
                    #sleeps for 15 minutes
                    time.sleep(900)
                    scraped.driver.get(url)
                    #getting item names and urls
                    items = scraped.driver.find_elements(By.CLASS_NAME, 'sku-title [href]')
                    links = [item.get_attribute('href') for item in items]
                    #getting statuses for stock
                    statuses = scraped.driver.find_elements(By.CLASS_NAME, "fulfillment-fulfillment-summary")
                    #get price 
                    prices = scraped.driver.find_elements(By.CLASS_NAME, 'priceView-hero-price.priceView-customer-price')
                await message.channel.send(f'@{message.author}:\n{links[ind]}')
                break
            except: 
                await message.channel.send("Enter a number please")
                pass

client.run(TOKEN)