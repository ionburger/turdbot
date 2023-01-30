import discord
from discord.ext import bridge, commands
from yt_dlp import YoutubeDL
from bin.storage import Config

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def qhandler(error=None,self=None, ctx=None, st=None):
        try:
            queue = (st.read("voice", "queue")).split("/./")
            queue.pop(0)
            st.write("voice", "queue", "/./".join(queue))
        except ValueError:
            ctx.voice_client.stop()
            return
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }
        ctx.voice_client.play(discord.FFmpegPCMAudio(queue[0].get("url",None), **ffmpeg_options), after=self.qhandler(self, ctx))
        ctx.respond(f"Now playing: {queue[0].get('title',None)}")

    @bridge.bridge_command()
    async def join(self, ctx):
        await ctx.defer()
        if ctx.author.voice is None:
            await ctx.respond("You are not in a voice channel")
        else:
            channel = ctx.author.voice.channel
            await channel.connect()
        
    @bridge.bridge_command()
    async def leave(self, ctx):
        await ctx.defer()
        st = Config(ctx.guild.id, self.bot.db)
        st.write("voice", "queue", "")
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            await ctx.voice_client.disconnect()
    
    @bridge.bridge_command()
    async def play(self, ctx, *, video: str):
        await ctx.defer()
        args = video.split(" ")
        channel = ""
        for arg in range(len(args)-1):
            if args[arg] == "-channel" or args[arg] == "-c":
                channel = discord.utils.get(ctx.guild.channels, name=args.pop(arg+1)).id
                args.pop(arg)
                break
        if channel != "" and ctx.author.guild_permissions.administrator == False:
            await ctx.respond("You do not have permission to specify a channel")
            return
        link = " ".join(args)
        if ctx.author.voice is None and channel == "":
            await ctx.respond("You are not in a voice channel, to specify a channel use `play <link> -channel <channel>`")
            return
        if ctx.voice_client is None:
            channel = ctx.author.voice.channel
            await channel.connect()
        if link == "":
            ctx.voice_client.resume()
            return
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }
        ytdl_format_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            }
        with YoutubeDL(ytdl_format_options) as ydl:
            st = Config(ctx.guild.id, self.bot.db)
            if link.startswith("https://"):
                info_dict = ydl.extract_info(link, download=False)
                video_url = info_dict.get("url", None)
                video_id = info_dict.get("id", None)
                video_title = info_dict.get('title', None)
            else:
                info_dict = ydl.extract_info(f"ytsearch:{link}", download=False)["entries"][0]
                video_url = info_dict.get("url", None)
                video_id = info_dict.get("id", None)
                video_title = info_dict.get('title', None)
        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(discord.FFmpegPCMAudio(video_url, **ffmpeg_options), after=self.qhandler(self=self, ctx=ctx, st=st))
            await ctx.respond(f"Now playing: {video_title}")
        else:
            queue = st.read("voice", "queue").split("/./")
            queue.append(info_dict)
            st.write("voice", "queue", "/./".join(queue))
        
    @bridge.bridge_command(alias=["stop"])
    async def pause(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            ctx.voice_client.pause()
            await ctx.respond("Paused")

    @bridge.bridge_command()
    async def skip(self, ctx):
        await ctx.defer()
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            ctx.voice_client.stop()
            await ctx.respond("Skipped")

def setup(bot):
    bot.add_cog(Voice(bot))        

    