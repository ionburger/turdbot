# Copyright (c) 2022, Ian Burgess
# All rights reserved.
#
# This source code is licensed under the GPLv3 license. A copy of this license can be found in the LICENSE file in the root directory of this source tree.
import asyncio
import logging
import yt_dlp
import random
import datetime
import datetime
import shelve
import backports.zoneinfo as zoneinfo
from bin.storage import config
import bin.version as version
import discord
from discord.ext import tasks, bridge as commands
logging.basicConfig(level=logging.INFO)


def run(update):

    quotetime = datetime.time(hour=12, tzinfo=zoneinfo.ZoneInfo("MST"))
    avgtimelst = []

    token = open("config/TOKEN", "r").read()
    intents = discord.Intents.all()
    bot = commands.Bot(intents=intents, command_prefix=".")


    # on ready
    @bot.event
    async def on_ready():
        print('logged in as {0.user}'.format(bot))
        print("discord.py version",discord.__version__)
        print("turdbot version",version.local())

        if not dailyquote.is_running():
            dailyquote.start()

    async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):  # Our voice client already passes these in.
        recorded_users = [  # A list of recorded users
            f"<@{user_id}>"
            for user_id, audio in sink.audio_data.items()
        ]
        files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]  # List down the files.




    @bot.bridge_command(description="aaa")
    async def eee(ctx):
        for guild in bot.guilds:
            await ctx.respond(guild.id)

    @bot.bridge_command(name="play")
    async def play(ctx, link: str):
            channel = ctx.author.voice.channel
            vc = await channel.connect()
            ytdl_format_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            }
            with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
                    info_dict = ydl.extract_info(link, download=False)
                    video_url = info_dict.get("url", None)
                    video_id = info_dict.get("id", None)
                    video_title = info_dict.get('title', None)
            vc.play(discord.FFmpegPCMAudio(video_url))

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
                    replys = config("triggerbotreplys", db="data")
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
