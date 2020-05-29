from discord.ext import commands


class PingPong(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send('pong')


def setup(bot):
    bot.add_cog(PingPong(bot))
