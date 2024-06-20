from discord.ext import bridge, commands
from bin.storage import storage

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        store = storage(message.guild.id, self.bot.db).store
        count = int(await store('counting', 'count') or 0)

        if message.author.bot or message.channel.id != await store('counting', 'channel') or not message.content.isdigit():
            return

        elif message.author.id == await store('counting', 'user'):
            await message.reply(f"you done fucked up there chief, you cant count twice")
        
        elif str(count+1) != message.content:
            await message.reply(f"you done fucked up there chief, count was {count}")
        
        else:
            await store('counting', 'count', count+1)
            await store('counting', 'user', message.author.id)
            await message.add_reaction('✅')
        

    @bridge.bridge_command()
    async def channel(self, ctx):
        store = storage(ctx.guild.id, self.bot.db).store
        await store('counting', 'channel', ctx.channel.id)
        await ctx.send(f"counting channel set to {await store('counting', 'channel')}")
    
    @bridge.bridge_command()
    async def setcount(self, ctx, args):
        store = storage(ctx.guild.id, self.bot.store).store
        await store('counting', 'count', args)
        await ctx.send(f"count set to {args}")

        


def setup(bot):
    bot.add_cog(Counting(bot))