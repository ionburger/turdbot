# Copyright (c) 2022, Ian Burgess
# All rights reserved.
#
# This source code is licensed under the GPLv3 license. A copy of this license can be found in the LICENSE file in the root directory of this source tree.

import discord
import random
import datetime
import shelve
import datetime
import shelve
import backports.zoneinfo as zoneinfo
from py.storage import config
from discord.ext import tasks, commands


quotetime = datetime.time(hour=12, tzinfo=zoneinfo.ZoneInfo("MST"))
avgtimelst = []

token = open("py/TOKEN", "r").read()
intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix=".")


# bot info
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


# main event
@bot.event
async def on_message(message):
    # defining variables
    msg = str(message.content)
    channel = str(message.channel.id)
    server = message.guild.id
    author = str(message.author)

    # reply to bots
    if message.author.bot and config("replytobot") == "false":
        return

    # start event timer
    print("\n start client.event")
    start = datetime.datetime.now()

    # triggerbot
    if config("triggerbotenabled") == "true":
        x = 0
        found = "false"
        triggers = config("triggerbottriggers", db="data")
        while x < len(triggers) and found == "false":
            if triggers[x] not in msg:
                x = x+1
            elif triggers[x] in msg:
                found = "true"
                replys = config(triggerbotreplys, db=data)
                rand = random.randint(0, len(replys))-1
                await message.channel.send(replys[rand])
            else:
                print("something happened")

    # daily quote
    if channel == config("quotequeue") and config("quotebotenabled") == "true":
        file = open("data/quotes.var", "a")
        file.write(msg)
        file.write(":")
        file.close()

    # bot commands
    await bot.process_commands(message)

    # end function timer
    end = datetime.datetime.now()
    eventime = (end - start)
    microseconds = eventime.microseconds
    avgtimelst.append(microseconds)
    avgtime = sum(avgtimelst) / len(avgtimelst)
    print("\n end client.event \n microseconds: " +
          str(microseconds) + "\n average time: " + str(avgtime))


@tasks.loop(time=quotetime, reconnect=True)
async def dailyquote():
    if config("quotebotenabled") == "true":
        file = open("data/quotes.var", "r+")
        list = file.read().split(":")
        rand = random.randint(0, (len(list)-1))
        print(rand)
        channel = bot.get_channel(int(quotebotconf["config"]["dailyquote"]))
        await channel.send(list.pop(rand))
        file.write(":".join(list))
        file.close()


bot.run(token)
