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