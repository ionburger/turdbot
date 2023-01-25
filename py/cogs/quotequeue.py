import discord
from discord.ext import commands, tasks

import datetime
from zoneinfo import ZoneInfo

from bin.storage import Config

times = [datetime.time(12,0,tzinfo=ZoneInfo("America/Denver"))]

class Quotequeue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.quotetime.start()
        print(self.quotetime.next_iteration)
    
    @tasks.loop(time=times)
    async def quotetime(self):
        channel = self.bot.get_channel(1004178748205187086)
        await channel.send("test")
    
    @quotetime.before_loop
    async def before_quotetime(self):
        await self.bot.wait_until_ready()
        print(self.quotetime.next_iteration)
        
def setup(bot):
    bot.add_cog(Quotequeue(bot))
