import configparser
import discord
from discord.ext import bridge
import discord
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.WARNING)

config = configparser.ConfigParser()
config.read("config/bot.conf")


bot = bridge.Bot(
    help_command=None,
    command_prefix="!",
    intents=discord.Intents.all(),
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="you")
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

    bot.load_extension("cogs.reply")
    bot.load_extension("cogs.repost")
    # bot.load_extension("cogs.counting")
    # bot.load_extension("cogs.test")

    
    bot.db = MongoClient(config["DATABASE"]["uri"])["main"]


bot.run(config["MAIN"]["token"])