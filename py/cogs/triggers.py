import discord
from discord.ext import commands
import random
from bin.storage import Config

class Triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        st = Config(message.guild.id,self.bot.db)
        if message.author.bot == True and st.read("misc","replytobot") == "false" or st.read("triggers","enabled") == "false" or str(message.channel.id) in st.read("triggers","channelblacklist").split("."):
            return
        dict = st.read("triggers","triggers")
        for key in dict.keys():
            if key in message.content:
                replys = dict[key].split("/./")
                await message.channel.send(random.choice(replys))
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
        # elif dt.read("triggers","mode") == "strict":
        #     for trigger in triggers:
        #         if trigger == message.content:
        #             replys = dt.read("triggers","replys").split(".")
        #             rand = randint(0, len(replys))-1
        #             await message.channel.send(replys[rand])
                    
        



def setup(bot):
    bot.add_cog(Triggers(bot))
