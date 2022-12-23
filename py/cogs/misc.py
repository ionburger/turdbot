import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        print("test")


def setup(bot):
    bot.add_cog(Misc(bot))


    #     # bot commands
    #     await bot.process_commands(message)
    # @tasks.loop(time=quotetime, reconnect=True)
    # async def dailyquote():
    #     if config("quotebotenabled") == "true":
    #         file = open("data/quotes.var", "r+")
    #         list = file.read().split(":")
    #         rand = random.randint(0, (len(list)-1))
    #         print(rand)
    #         channel = bot.get_channel(int(quotebotconf["config"]["dailyquote"]))
    #         await channel.send(list.pop(rand))
    #         file.write(":".join(list))
    #         file.close()

    #          @bot.event
    # async def on_ready():
    #     print('logged in as {0.user}'.format(bot))
    #     print("pycord version",discord.__version__)
    #     print("turdbot version",version.local())

