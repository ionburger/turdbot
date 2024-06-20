from discord.ext import bridge, commands
from bin.storage import storage

class Triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        store = storage(message.guild.id, self.bot.db).store
        if await store('triggers', 'enabled') == "True":
            for trigger in await store('triggers', 'triggers'):
                if trigger.lower() in message.content.lower():
                    await message.reply(store('triggers', 'response'))

def setup(bot):
    bot.add_cog(Triggers(bot))