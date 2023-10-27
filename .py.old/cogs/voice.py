import discord
from discord.ext import bridge, commands
import wavelink
from bin.storage import Config

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = wavelink.Queue()

    @commands.Cog.listener()
    async def on_ready(self):
        await wavelink.NodePool.create_node(bot=self.bot,
                                            host=self.bot.config["wavelink"]["host"],
                                            port=self.bot.config["wavelink"]["port"],
                                            password=self.bot.config["wavelink"]["password"],)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player, track, reason):
        print("track ended")
        if not self.queue.is_empty and reason == 'FINISHED':
            await player.play(self.queue.get())

    @bridge.bridge_command(alises=["j"])
    async def join(self, ctx, *, args: str=""):
        await ctx.defer()
        if ctx.author.voice is None and args == "":
            await ctx.respond("You are not in a voice channel")
        elif args != "":
            channel = self.bot.get_channel(discord.utils.get(ctx.guild.channels, name=args).id)
            await channel.connect(cls=wavelink.Player)
        else:
            await ctx.author.voice.channel.connect(cls=wavelink.Player)
        
    @bridge.bridge_command(alises=["l"])
    async def leave(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            await ctx.voice_client.disconnect()
    
    @bridge.bridge_command(aliases=["p"])
    async def play(self, ctx, *, link: str=""):
        await ctx.defer()
        providedchannel = False
        queueoverride = False
        earape = False
        channel = ""
        args = link.split(" -")
        if len(args) > 1:
            for arg in range(len(args)):
                if args[arg].startswith("channel") or args[arg].startswith("c"):
                    channel = self.bot.get_channel(discord.utils.get(ctx.guild.channels, name=args[arg].split(" ")[1]).id)
                    providedchannel = True
                if args[arg].startswith("now") or args[arg].startswith("n"):
                    queueoverride = True
                if args[arg].startswith("earrape") or args[arg].startswith("e"):
                    earape = True
        track = await wavelink.YouTubeTrack.search(args[0], return_first=True)

        
        if providedchannel and ctx.author.guild_permissions.administrator == False:
            await ctx.respond("You do not have permission to specify a channel")
            return
        if queueoverride and ctx.author.guild_permissions.administrator == False:
            await ctx.respond("You do not have permission to override the queue")
            return
        if earape and ctx.author.guild_permissions.administrator == False:
            await ctx.respond("You do not have permission to earrape")
            return
        
        
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
        
        if (self.queue.is_empty and not ctx.voice_client.is_playing()) or queueoverride:
            #not implemented
            #if earape:
                #print("earrape")
                #await ctx.voice_client.set_filter(wavelink.Filter(distortion=wavelink.Distortion(sin_offset=2,sin_scale=2,tan_offset=3)),seek=True)

            await ctx.voice_client.play(track)
            await ctx.respond(f"Now playing: {track.title} by {track.author}\n {track.uri}")
        else:
            self.queue.put(item=track)
            await ctx.respond(f"Added to queue: {track.title} by {track.author}\n {track.uri}") 
        
    @bridge.bridge_command(aliases=["stop","s"])
    async def pause(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            await ctx.voice_client.pause()
            await ctx.respond("Paused")

    @bridge.bridge_command(aliases=["next","n","sk"])
    async def skip(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            await ctx.voice_client.play(self.queue.get())
            await ctx.respond("Skipped")

def setup(bot):
    bot.add_cog(Voice(bot))        