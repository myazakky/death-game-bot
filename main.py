from discord.ext import commands
import config

bot = commands.Bot(command_prefix='!')

if __name__ == '__main__':
    bot.run(config.token)
