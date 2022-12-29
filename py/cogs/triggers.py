import discord
from discord.ext import commands
from random import randint
from bin.storage import *

class Triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        dt = Data(str(message.guild.id))
        st = Config(str(message.guild.id))

        if message.author.bot == True and st.read("misc","replytobot") == "false" or st.read("triggers","enabled") == "false" or str(message.channel.id) in st.read("triggers","channelblacklist",).split("."):
            print("return")
            return

        print("triggers")
        triggers = dt.read("triggers","triggers").split("/./")
        replys = dt.read("triggers","replys").split("/./")


        if st.read("triggers","mode") == "normal":
            for trigger in triggers:
                if trigger in message.content:
                    rand = randint(0, len(replys))-1
                    await message.channel.send(replys[rand])
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
        # elif dt.read("triggers","mode") == "strict":
        #     for trigger in triggers:
        #         if trigger == message.content:
        #             replys = dt.read("triggers","replys").split(".")
        #             rand = randint(0, len(replys))-1
        #             await message.channel.send(replys[rand])
                    
        



def setup(bot):
    bot.add_cog(Triggers(bot))
