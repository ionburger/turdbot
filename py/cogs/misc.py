import discord
from discord.ext import commands

from bin.storage import Config

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}\nPycord version {discord.__version__}\nTurdbot version {self.bot.version}\n")
        for guild in self.bot.guilds:
            st = Config(guild.id,self.bot.db)
            st.updateguild()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        st = Config(guild.id,self.bot.db)
        st.updateguild()







def setup(bot):
    bot.add_cog(Misc(bot))