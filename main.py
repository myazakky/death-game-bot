from discord.ext import commands
import config
import pathlib

bot = commands.Bot(command_prefix='!')

cog_file_paths = pathlib.Path('./cogs/').glob('*.py')

for path in list(cog_file_paths):
    str_path = str(path).replace('/', '.').replace('.py', '')
    bot.load_extension(str_path)

if __name__ == '__main__':
    bot.run(config.token)
