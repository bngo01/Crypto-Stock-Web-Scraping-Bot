import discord
import requests
import bs4
import threading
from datetime import datetime
from discord.ext import commands

# Bot prefix
bot = commands.Bot(command_prefix = "!")

def update_time():
    '''Constantly updates time'''
    threading.Timer(1, update_time).start()
    time = datetime.now()
    return time

@bot.command()
async def ping(context):
    '''Tests the bot's internet connection'''
    await context.channel.send("{} ms".format(round(bot.latency * 1000)))

@bot.command()
async def clear(context):
    '''Delete all previous commands in channel'''
    await context.channel.purge(limit = 1000000000000000)
    await context.channel.send("Clear successful.")

@bot.command()
async def time(context):
    '''Displays time and date'''
    time = update_time()
    await context.channel.send("It is currently {}".format(time.strftime(r"%I:%M:%S%p EST on %m/%d/%y")))

@bot.command()
async def crypto(context, *args):
    '''Web scrapes crypto information'''
    crypto_url = "https://markets.businessinsider.com/currencies/{}-usd".format(args[0])
    html_content = requests.get(crypto_url).text
    soup = bs4.BeautifulSoup(html_content, "lxml")

    # Command input validation
    if len(args) == 2:
        # Check user request
        if args[1] == "price":
            # Update time
            threading.Timer(1, crypto).start()
            time = update_time()

            # Web scrape data
            price = soup.find("span", class_ = "price-section__current-value")

            # Creating Embed
            output_embed = discord.Embed(title = "Crypto Data: ", description = "{} Price: ${}\nUpdated as of {}".format(args[0], price.text, time.strftime(r"%m/%d/%y %I:%M:%S%p EST")), color = 0xff0000)
            output_embed.set_footer(text = "Data Provided by Business Insider (markets.businessinsider.com)")
            # Displaying Embed
            await context.channel.send(embed = output_embed)
    else:
        await context.channel.send("Please enter the command corrently e.g. !crypto BTC price")

@bot.command()
async def stock(context, *args):
    '''Web scrapes stock information'''
    stock_url = "https://markets.businessinsider.com/stocks/{}-stock".format(args[0])
    html_content = requests.get(stock_url).text
    soup = bs4.BeautifulSoup(html_content, "lxml")

    # Command input validation
    if len(args) == 2:
        # Check user request
        if args[1] == "price":
            # Update time
            threading.Timer(1, stock).start()
            time = update_time()
            
            # Web scrape data
            price = soup.find("span", class_ = "price-section__current-value")

            # Creating Embed
            output_embed = discord.Embed(title = "Stock Data: ", description = "{} Price: ${}\nUpdated as of {}".format(args[0], price.text, time.strftime(r"%m/%d/%y %I:%M:%S%p EST")), color = 0xff0000)
            output_embed.set_footer(text = "Data Provided by Business Insider (markets.businessinsider.com)")
            # Displaying Embed
            await context.channel.send(embed = output_embed)
    else:
        await context.channel.send("Please enter the command correctly e.g. !stock AAPL price")

@bot.event
async def on_ready():
    general_channel = bot.get_channel(930820714485915652)

    # Welcome message
    await general_channel.send("{} has entered the chat!".format(bot.user))
    welcome_embed = discord.Embed(title = "Welcome to pybot web scraping server!", description = "Currently, this bot will web scrape stock/crypto prices and display it in an embed.\n\nFormat: ![crypto/stock] [ticker] price \ne.g. !crypto BTC price \ne.g. !stock AAPL price", color = 0x00ff00)
    welcome_embed.set_author(name = "Bao Ngo")
    welcome_embed.set_footer(text = "Data Provided by Business Insider (markets.businessinsider.com)")
    await general_channel.send(embed = welcome_embed)

# Run bot
# Token removed for security purposes
bot.run("place token here")