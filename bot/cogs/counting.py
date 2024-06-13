from discord.ext import bridge, commands
from bin.storage import storage

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        db = storage(message.guild.id, self.bot.db).db
        count = int(db('counting', 'count') or 0)

        if message.author.bot or message.channel.id != db('counting', 'channel') or not message.content.isdigit():
            return

        elif message.author.id == db('counting', 'user'):
            await message.reply(f"you done fucked up there chief, you cant count twice")
        
        elif str(count+1) != message.content:
            await message.reply(f"you done fucked up there chief, count was {count}")
        
        else:
            db('counting', 'count', count+1)
            db('counting', 'user', message.author.id)
            await message.add_reaction('✅')
        

    @bridge.bridge_command()
    async def channel(self, ctx):
        db = storage(ctx.guild.id, self.bot.db).db
        db('counting', 'channel', ctx.channel.id)
        await ctx.send(f"counting channel set to {db('counting', 'channel')}")
    
    @bridge.bridge_command()
    async def setcount(self, ctx, args):
        db = storage(ctx.guild.id, self.bot.db).db
        db('counting', 'count', args)
        await ctx.send(f"count set to {args}")

        


def setup(bot):
    bot.add_cog(Counting(bot))