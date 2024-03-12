from os import environ as env
import discord
from discord.ext import bridge
import logging
from pymongo import MongoClient
from bin.storage import storage

logging.basicConfig(filename="turdbot.log",level=logging.INFO)

bot = bridge.Bot(
    help_command=None,
    command_prefix="!",
    intents=discord.Intents.all(),
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="you")
)

bot.load_extension("cogs.reply")
bot.load_extension("cogs.counting")

uri = f"mongodb://{env['DB_USERNAME']}:{env['DB_PASSWORD']}@{env['DB_HOST']}/?authSource=admin"
bot.db = MongoClient(uri)["turdbot"]

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    # logging.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    # for guild in bot.guilds:
    #     logging.info(f"Added {guild.name} (ID: {guild.id})")
    #     storage(guild.id, bot.db).update_guild()


bot.run(env["BOT_TOKEN"])