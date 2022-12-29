import discord
from discord.ext import bridge, tasks
import logging
import argparse
import os

#logging
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

#intents and cogs
intents = discord.Intents.all()
bot = bridge.Bot(intents=intents,command_prefix=".")
# for filename in os.listdir("cogs"):
#     if filename.endswith(".py"):
#         bot.load_extension(f"cogs.{filename[:-3]}")
bot.load_extension("cogs.counting")
bot.load_extension("cogs.triggers")

@bot.event
async def on_ready():
    print("ready")

    
bot.run("MTA1MjY4Mjk3NjE4NzY1NDIzNQ.GhBNf-.E4QTCbJZ5KdELV6628dPeBnbq5Tjhx3Y0Ig5fA")