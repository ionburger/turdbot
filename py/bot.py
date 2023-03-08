import discord
from discord.ext import bridge, tasks
from pymongo import MongoClient
import logging
import argparse
import configparser

log = logging.getLogger(__name__)


#setup
intents = discord.Intents.all()
bot = bridge.Bot(intents=intents,command_prefix=".")
config = configparser.ConfigParser()
config.read("config/config.conf")
bot.config = config
bot.db = MongoClient(config["mongodb"]["host"],int(config["mongodb"]["port"]),username=config["mongodb"]["username"],password=config["mongodb"]["password"])["dev"]
bot.version = "2.0.0"
bot.load_extension("cogs.counting")
bot.load_extension("cogs.misc")
bot.load_extension("cogs.triggers")
bot.load_extension("cogs.dad")
bot.load_extension("cogs.voice")
#bot.load_extension("cogs.quotequeue")


#logging
parser = argparse.ArgumentParser()
parser.add_argument("-d","--debug", action="store_true")
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename='logs/bot.log',filemode='w')

            
else:
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',filename='logs/bot.log',
      filemode='w')


bot.run(config["config"]["token"])