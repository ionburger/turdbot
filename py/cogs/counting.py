import discord
from discord.ext import commands
from bin.storage import storage 

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        serverid = message.guild.id
        if message.author.bot or str(message.channel.id) != storage("counting","countingchannel",) or not message.content.isnumeric():
            print("return")
            return
        print(storage("counting","countingcount"))

        if int(message.content) == int(storage("counting","countingcount"))+1 and str(message.author) != storage("counting","countinguser",):
            storage("counting","countingcount",message.content,mode="w")
            storage("counting","countinguser",message.author,mode="w")
        elif int(message.content) == int(storage("counting","countingcount"))+1 and str(message.author) == storage("counting","countinguser",):
            await message.channel.send("A user cannot count twice in a row, counting reset to 1")
            storage("counting","countingcount",0,mode="w")
            storage("counting","countinguser","None",mode="w")
        elif int(message.content) != int(storage("counting","countingcount"))+1:
            await message.channel.send("Wrong number, counting reset to 1")
            storage("counting","countingcount",0,mode="w")
            storage("counting","countinguser","None",mode="w")
def setup(bot):
    bot.add_cog(Counting(bot))
