import discord
from discord.ext import commands

from bin.storage import Config

class Dad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        st = Config(str(message.guild.id),self.bot.db)
        if message.author.bot == True or st.read("dad","enabled") == "false":
            return
        msg = message.content.split(" ")
        for i in range(len(msg)):
            if msg[i].lower() == "i'm" or msg[i].lower() == "im":
                await message.channel.send(f"Hi {msg[i+1]}, I'm Dad")
                return



def setup(bot):
    bot.add_cog(Dad(bot))