from discord.ext import bridge, commands
import discord
import opencv
from bin.imagematcher import imagematcher

class Repost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge.bridge_command()
    async def repost(self, ctx):
        referenceimgurl = ctx.channel.fetch_message(ctx.message.reference.message_id).attachments[0].url
        msgs = await ctx.channel.history(limit=50).flatten()
        for msg in msgs:
            for attachment in msg.attachments:
                if imagematcher(attachment.url, referenceimgurl) < 90:
                    await ctx.send(attachment.url)
def setup(bot):
    bot.add_cog(Repost(bot))