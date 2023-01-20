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
        dict = st.read("triggers","data")
        for k,v in dict.items():
            if v["mode"] == "lax":
                if k in message.content:
                    await message.channel.send(random.choice(v["replys"].split("/./")))
            elif v["mode"] == "normal":
                if k in message.content.split(" "):
                    await message.channel.send(random.choice(v["replys"].split("/./")))
            elif v["mode"] == "strict":
                if k == str(message.content):
                    await message.channel.send(random.choice(v["replys"].split("/./")))       
       
def setup(bot):
    bot.add_cog(Triggers(bot))
