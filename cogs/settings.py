from discord.ext import bridge, commands
from bin.storage import storage

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group(aliases=["set", "s"], invoke_without_command=True)
    async def settings(self, ctx):
        await ctx.respond("invalid command, see !help settings for more info")
    
    @settings.command()
    



def setup(bot):
    bot.add_cog(Settings(bot))

