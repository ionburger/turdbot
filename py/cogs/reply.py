from discord.ext import bridge, commands

class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    async def reply(self, ctx, *args):
        await ctx.send(args)

def setup(bot):
    bot.add_cog(Reply(bot))