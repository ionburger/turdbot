import discord
from discord.ext import commands, tasks

import datetime

from bin.storage import Config



class Quotequeue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.quotequeue.start()
    
    @tasks.loop(seconds=5)
    async def quotequeue(self):
        channel = self.bot.get_channel(1004178748205187086)
        await channel.send("test")
    
    @quotequeue.before_loop
    async def before_quotequeue(self):
        await self.bot.wait_until_ready()
        
def setup(bot):
    bot.add_cog(Quotequeue(bot))
