from os import environ as env
import discord
from discord.ext import bridge
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from bin.storage import storage

bot = bridge.Bot(
    help_command=None,
    command_prefix="!",
    intents=discord.Intents.all(),
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="you")
)

bot.load_extension("cogs.triggers")
bot.load_extension("cogs.counting")
bot.load_extension("cogs.settings")

uri = f"mongodb://{env['DB_USERNAME']}:{env['DB_PASSWORD']}@{env['DB_HOST']}/?authSource=admin"
bot.db = MongoClient(uri)["turdbot"]

bot.version = "4.0.0ALPHA"

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

bot.run(env["BOT_TOKEN"])