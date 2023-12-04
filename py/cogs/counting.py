from discord.ext import bridge




def setup(bot):
    bot.add_cog(Counting(bot))