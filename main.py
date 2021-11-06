from nextcord.ext import commands
from yaml import load as load_yaml

def load_config():
    with open('config.yml') as file:
        data = file.read()
        load_yaml(data)
    return data

config = load_config()

bot = commands.Bot(command_prefix=config.prefix)

@bot.command()
async def ping(ctx):
    await ctx.reply('Pong!')

bot.run(config.token)