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
    
    @commands.Cog.listener()
    async def on_message(self, message):
        st = Config(message.guild.id,self.bot.db)
        if message.author.bot == True and st.read("misc","replytobot") == "false":
            return
        if str(message.content) == ("r"):
            self.bot.reload_extension("cogs.misc")
            self.bot.reload_extension("cogs.triggers")
            self.bot.reload_extension("cogs.counting")
            #self.bot.reload_extension("cogs.quotequeue")
            self.bot.reload_extension("cogs.voice")
            st = Config(message.guild.id,self.bot.db)
            st.updateguild()
            await message.channel.send("r")








def setup(bot):
    bot.add_cog(Misc(bot))