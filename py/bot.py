import discord
from discord.ext import bridge, tasks
import logging
import argparse
import os
from pynput import keyboard



#intents and cogs
intents = discord.Intents.all()
bot = bridge.Bot(intents=intents,command_prefix=".")
token = open("data/TOKEN","r").read()
# for filename in os.listdir("cogs"):
#     if filename.endswith(".py"):
#         bot.load_extension(f"cogs.{filename[:-3]}")
bot.load_extension("cogs.counting")
bot.load_extension("cogs.triggers")


#logging
parser = argparse.ArgumentParser()
parser.add_argument("-d","--debug", action="store_true")
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
    def on_press(key):
        if key == keyboard.KeyCode.from_char('r'):
            bot.unload_extension("cogs.counting")
            bot.load_extension("cogs.counting")
            print("reloaded counting")
            bot.unload_extension("cogs.triggers")
            bot.load_extension("cogs.triggers")
            print("reloaded triggers")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
            
else:
    logging.basicConfig(level=logging.INFO)



@bot.event
async def on_ready():
    print("ready")


bot.run(token)