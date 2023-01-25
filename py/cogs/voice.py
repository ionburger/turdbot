import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
from bin.storage import Config

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    def player(self, ctx):
        print(self.queue)
        if len(self.queue) == 0:
            return
        self.queue.pop(0)
        ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        ctx.voice_client.play(discord.FFmpegPCMAudio(self.queue[0], **ffmpeg_options), after=Voice.player(self, ctx))
        

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
    async def play(self, ctx, link):
        if ctx.author.voice is None:
            await ctx.respond("You are not in a voice channel")
        if ctx.voice_client is None:
            channel = ctx.author.voice.channel
            await channel.connect()
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
            info_dict = ydl.extract_info(f"ytsearch:{link}", download=False)["entries"][0]
            video_url = info_dict.get("url", None)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
            self.queue.append(video_url)
        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(discord.FFmpegPCMAudio(self.queue[0], **ffmpeg_options), after=Voice.player(self, ctx))
        

def setup(bot):
    bot.add_cog(Voice(bot))
