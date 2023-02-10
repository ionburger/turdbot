import discord
from discord.ext import bridge, commands
import wavelink
from bin.storage import Config

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await wavelink.NodePool.create_node(bot=self.bot,
                                            host=self.bot.config["wavelink"]["host"],
                                            port=self.bot.config["wavelink"]["port"],
                                            password=self.bot.config["wavelink"]["password"],)

    def qhandler(error=None,self=None, ctx=None, st=None):
        print("test")
        queue = (st.read("voice", "queue")).split("/./")
        try:
            queue.pop(0)
        except:
            pass
        st.write("voice", "queue", "/./".join(queue))
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }
        if len(queue) > 0:
            ctx.voice_client.play(discord.FFmpegPCMAudio(queue[0]), **ffmpeg_options, after=self.qhandler(self, ctx))
            ctx.respond(f"Now playing: {queue[0]}")
    
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
        st = Config(ctx.guild.id, self.bot.db)
        st.write("voice", "queue", "")
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            await ctx.voice_client.disconnect()
    
    @bridge.bridge_command(aliases=["p"])
    async def play(self, ctx, *, link: str):
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

        if ctx.author.voice is None and channel == "":
            await ctx.respond("You are not in a voice channel, to specify a channel use `play <link> -channel <channel>`")
            return

        if ctx.voice_client is None:
            if channel == "":
                channel = ctx.author.voice.channel
            vc = await channel.connect(cls=wavelink.Player)

        if link == "" and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            return

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        await vc.play(await wavelink.YouTubeTrack.search(link,return_first=True))
        await ctx.respond(f"Now playing: {link}")
        # ffmpeg_options = {
        #     'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        #     'options': '-vn'
        #     }
        # if not ctx.voice_client.is_playing():
        #     ctx.voice_client.play(discord.FFmpegPCMAudio(video_url, **ffmpeg_options), after=self.qhandler(self=self, ctx=ctx, st=st))
        #     await ctx.respond(f"Now playing: {video_title}")
        # else:
        #     print("Added to queue")
        #     queue = st.read("voice", "queue").split("/./")
        #     queue.append(info_dict.get("url",None))
        #     st.write("voice", "queue", "/./".join(queue))
        #     await ctx.respond(f"Added to queue: {video_title}")
        
    @bridge.bridge_command(aliases=["stop"])
    async def pause(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            await ctx.voice_client.pause()
            await ctx.respond("Paused")

    @bridge.bridge_command(alias=["next", "n","s"])
    async def skip(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            ctx.voice_client.stop()
            await ctx.respond("Skipped")

def setup(bot):
    bot.add_cog(Voice(bot))        

