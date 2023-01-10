import discord
from discord.ext import commands

from bin.storage import Config

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        st = Config(str(message.guild.id),self.bot.db)
        if message.author.bot == True or st.read("counting","enabled") == "false" or str(message.channel.id) != st.read("counting","countingchannel",) or not message.content.isnumeric():
            return

        if int(message.content) == int(st.read("counting","countingcount"))+1 and str(message.author) != st.read("counting","countinguser",):
            st.write("counting","countingcount",message.content)
            st.write("counting","countinguser",message.author)
        elif int(message.content) == int(st.read("counting","countingcount"))+1 and str(message.author) == st.read("counting","countinguser",):
            await message.channel.send("A user cannot count twice in a row, counting reset to 1")
            st.write("counting","countingcount",0)
            st.write("counting","countinguser","None")
        elif int(message.content) != int(st.read("counting","countingcount"))+1:
            await message.channel.send("Wrong number, counting reset to 1")
            st.write("counting","countingcount",0)
            st.write("counting","countinguser","None")
def setup(bot):
    bot.add_cog(Counting(bot))
