from discord.ext import bridge, commands
from bin.storage import storage

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    async def ping(self, ctx):
        await ctx.send(f"pong! {round(self.bot.latency * 1000)}ms")

    @bridge.bridge_command()
    async def version(self, ctx):
        await ctx.send(self.bot.version)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print(self.bot.version)
        print("------")


def setup(bot):
    bot.add_cog(Misc(bot))