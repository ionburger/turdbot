#imports
import discord
import random
import configparser
import backports.zoneinfo as zoneinfo
import datetime
from datetime import time
from discord.ext import tasks, commands


#glob vars
quotetime = datetime.time(hour=12,tzinfo=zoneinfo.ZoneInfo("MST"))


#loading config files
botconf = configparser.ConfigParser()
botconf.read("config/bot.conf")
triggerbotconf = configparser.ConfigParser()
triggerbotconf.read("config/triggerbot.conf")
quotebotconf = configparser.ConfigParser()
quotebotconf.read("config/quotebot.conf")


#bot info
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    if not dailyquote.is_running():
        dailyquote.start()
print("discord.py version")
print(discord.__version__)


@bot.command()
async def foo(ctx):
    for guild in bot.guilds:
        await ctx.send(guild.id)


#main event
@bot.event
async def on_message(message):
    #defining variables
    msg = str(message.content)
    channel = str(message.channel.id)
    author = str(message.author)
    

    #reply to bots
    if message.author.bot and botconf["config"]["replytobot"] == "false": 
        return


    #start event timer
    print("\n start client.event")
    start = time.time()


    #triggerbot
    if triggerbotconf["config"]["enabled"] == "true":
        x = 0
        found = "false"
        triggersstr = (triggerbotconf["config"]["triggers"])
        triggers = triggersstr.split(",")
        while x < len(triggers) and found == "false": 
            if triggers[x] not in msg:
                x = x+1
            elif triggers[x] in msg:
                found = "true"
                replys = triggerbotconf["replys"][triggers[x]].split(",")
                rand = random.randint(0,len(replys))-1
                await message.channel.send(replys[rand])
            else:
                print("something happened")
        

    #daily quote
    if channel == quotebotconf["config"]["quotequeue"] and quotebotconf["config"]["enabled"] == "true":
        file = open("data/quotes.var","a")
        file.write(msg)
        file.write(":")
        file.close()

    #bot commands
    await bot.process_commands(message)


    #end function timer
    global avgtimelst
    avgtimelst = []
    end = time.time()
    reventime = str(round((end - start),3))
    avgtimelst.append(float(reventime))
    avgtime = str(sum(avgtimelst) / len(avgtimelst))
    print("\n end client.event \n time: " + str(reventime) + "\n average time: " + avgtime)


@tasks.loop(time=quotetime,reconnect=True)
async def dailyquote():
    if quotebotconf["config"]["enabled"] == "true":
        file = open("data/quotes.var","r+")
        list = file.read().split(":")
        rand = random.randint(0, (len(list)-1))
        print(rand)
        channel = bot.get_channel(int(quotebotconf["config"]["dailyquote"]))
        await channel.send(list.pop(rand))
        file.write(":".join(list))
        file.close()


intents = discord.Intents.all()
bot = commands.Bot(intents=intents,command_prefix=".")
bot.run(botconf["config"]["token"])
