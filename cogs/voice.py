from discord.ext import bridge, commands
from bin.storage import storage
from os import environ as env
import wavelink



class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        nodes = [
            wavelink.Node(
            identifier="Node1",
            uri="http://0.0.0.0:2333",
            password=env["LAVALINK_SERVER_PASSWORD"]  
            )
        ]

        await wavelink.Pool.connect(nodes=nodes, client=bot)
def setup(bot):
    bot.add_cog(Voice(bot))

