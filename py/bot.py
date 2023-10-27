import discord

bot = discord.Bot(
    help_command="help",
    command_prefix="!",
    intents=discord.Intents.all(),
    activity=discord.Activity(
        type=discord.ActivityType.playing,
        name="with deez nuts",
    )
)
bot.run("OTg2NDA4MjM3Njg5NjMwNzYx.GOWW5z.Engl7UzrUyQkmj0hwQi42U-Z-XQ8CZPuMQRFlU")