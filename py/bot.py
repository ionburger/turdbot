import discord
from discord.ext import bridge, tasks
import logging


intents = discord.Intents.all()
bot = bridge.Bot(intents=intents,command_prefix=".")
bot.load_extension("cogs.counting")
bot.load_extension("cogs.misc")

@bot.event
async def on_ready():
    print("ready")
    
bot.run("OTg2NDA4MjM3Njg5NjMwNzYx.GRYraL.xouKNXYuRw9KDuTLTpXjBDcjtXOuod4J4zgP60")