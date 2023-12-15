from discord.ext import bridge, commands
import discord
from bin.storage import storage

#import opencv
#from bin.imagematcher import imagematcher

class Repost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge.bridge_command()
    async def repost(self, ctx):
        st = storage("test", self.bot.db)
        #referenceimgurl = ctx.channel.fetch_message(ctx.message.reference.message_id).attachments[0].url
        msgs = await ctx.channel.history(limit=100).flatten()
        l = {}
        for msg in msgs:
            for attachment in msg.attachments:
                l[msg.id] = attachment.url
        st.db("test", "test", l)
def setup(bot):
    bot.add_cog(Repost(bot))