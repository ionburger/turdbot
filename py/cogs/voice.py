import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
from bin.storage import Config

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def qhandler(self, ctx, error=None):
        print(ctx.guild.id)
        st = Config(ctx.guild.id, self.bot.db)
        queue = st.read("voice", "queue").split("/./")
        queue.pop(0)
        st.write("voice", "queue", queue.join("/./"))
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }
        if len(queue) > 0:
            ctx.voice_client.play(discord.FFmpegPCMAudio(queue[0].get("url",None), **ffmpeg_options), after=self.qhandler(self, ctx))
            ctx.respond(f"Now playing: {queue[0].get('title',None)}")
        else:
            ctx.voice_client.stop()

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.respond("You are not in a voice channel")
        else:
            channel = ctx.author.voice.channel
            await channel.connect()
        
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            await ctx.voice_client.disconnect()
    
    @commands.command()
    async def play(self, ctx, link=""):
        if ctx.author.voice is None and channel == "":
            await ctx.respond("You are not in a voice channel, to specify a channel use `play <link> <channel>`")
            return
        if ctx.author.voice is None:
            channel = ctx.guild.get_channel(channel)
            await channel.connect()
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
            ctx.voice_client.play(discord.FFmpegPCMAudio(video_url, **ffmpeg_options), after=self.qhandler(self, ctx))
            await ctx.respond(f"Now playing: {video_title}")
        else:
            st = Config(ctx.guild.id, self.bot.db)
            queue = st.read("voice", "queue").split("/./")
            queue.append(info_dict)
            st.write("voice", "queue", queue.join("/./"))
        
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client is None:
            await ctx.respond("I am not in a voice channel")
        else:
            ctx.voice_client.pause()
            await ctx.respond("Paused")
def setup(bot):
    bot.add_cog(Voice(bot))        

    