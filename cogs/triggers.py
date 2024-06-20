from discord.ext import bridge, commands
from bin.storage import storage

class Triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        db = storage(message.guild.id, self.bot.db).db
        if db('triggers', 'enabled'):
            for trigger in db('triggers', 'triggers'):
                if trigger.lower() in message.content.lower():
                    await message.reply(db('triggers', 'response'))

def setup(bot):
    bot.add_cog(Triggers(bot))