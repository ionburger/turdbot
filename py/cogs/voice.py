import discord
from discord.ext import bridge, commands
import wavelink
from bin.storage import Config

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = wavelink.Queue

    @commands.Cog.listener()
    async def on_ready(self):
        await wavelink.NodePool.create_node(bot=self.bot,
                                            host=self.bot.config["wavelink"]["host"],
                                            port=self.bot.config["wavelink"]["port"],
                                            password=self.bot.config["wavelink"]["password"],)

    @commands.Cog.listener()
    async def on_track_end(self, player, track, reason):
        if not reason == wavelink.TrackEndReason.STOPPED or self.queue.is_empty:
            player.play(await self.queue.get())
    @bridge.bridge_command(alises=["j"])
    async def join(self, ctx):
        await ctx.defer()
        if ctx.author.voice is None:
            await ctx.respond("You are not in a voice channel")
        else:
            channel = ctx.author.voice.channel
            await channel.connect()
        
    @bridge.bridge_command(alises=["l"])
    async def leave(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            await ctx.voice_client.disconnect()
    
    @bridge.bridge_command(aliases=["p"])
    async def play(self, ctx, *, link: str=""):
        # await ctx.defer()
        # args = video.split(" ")
        # providedchannel = False
        channel = ""
        # for arg in range(len(args)-1):
        #     if args[arg] == "-channel" or args[arg] == "-c":
        #         channel = self.bot.get_channel(discord.utils.get(ctx.guild.channels, name=args.pop(arg+1)).id)
        #         print(type(channel))
        #         print(channel)
        #         args.pop(arg)
        #         providedchannel = True
        #         break
        # else:
        #     channel = ctx.author.voice.channel
        
        # link = " ".join(args)

        # if providedchannel and ctx.author.guild_permissions.administrator == False:
        #     await ctx.respond("You do not have permission to specify a channel")
        #     return
        track = await wavelink.YouTubeTrack.search(link, return_first=True)
        if ctx.author.voice is None and channel == "":
            await ctx.respond("You are not in a voice channel, to specify a channel use `play <link> -channel <channel>`")
            return

        if ctx.voice_client is None:
            if channel == "":
                channel = ctx.author.voice.channel
            await channel.connect(cls=wavelink.Player)

        if link == "" and ctx.voice_client.is_paused():
            await ctx.voice_client.resume()
            return

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        
        if self.queue.is_empty and not ctx.voice_client.is_playing():
            await ctx.voice_client.play(track)
            await ctx.respond(f"Now playing: {track.title} by {track.author}\n {track.uri}")
        
        else:
            await self.queue.put(item=track)
            await ctx.respond(f"Added to queue: {track.title} by {track.author}\n {track.uri}") 
        
    @bridge.bridge_command(aliases=["stop","s"])
    async def pause(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            await ctx.voice_client.pause()

    @bridge.bridge_command(aliases=["next","n","st"])
    async def skip(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            ctx.voice_client.play(await self.queue.get())
            await ctx.respond("Skipped")

def setup(bot):
    bot.add_cog(Voice(bot))        

