# Copyright (c) 2022, Ian Burgess
# All rights reserved.
#
# This source code is licensed under the GPLv3 license. A copy of this license can be found in the LICENSE file in the root directory of this source tree.
import asyncio
#from discord.sinks import WaveSink as PycordWaveSink, Filters, AudioData
from discord.sinks import Filters, AudioData
import speech_recognition as sr
r = sr.Recognizer()

import logging
import yt_dlp
import random
import datetime
import wave
import io
import backports.zoneinfo as zoneinfo
from bin.storage import config
import bin.version as version
import discord
from discord.ext import tasks, bridge
logging.basicConfig(level=logging.INFO)


def run(update=False):

    quotetime = datetime.time(hour=12, tzinfo=zoneinfo.ZoneInfo("MST"))
    avgtimelst = []
    countingcount = 0
    countinguser = ""

    token = open("config/TOKEN", "r").read()
    intents = discord.Intents.all()
    bot = bridge.Bot(intents=intents, command_prefix=".")

    # on ready
    @bot.event
    async def on_ready():
        print('logged in as {0.user}'.format(bot))
        print("pycord version",discord.__version__)
        print("turdbot version",version.local())

        if not dailyquote.is_running():
            dailyquote.start()

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

       

      






    bot.run(token)
