from nextcord.embeds import Embed
from nextcord.ext import commands
from yaml import load as load_yaml, Loader
from math import floor
import pickledb

db = pickledb.load('')

def load_config():
    with open('config.yml') as file:
        data = file.read()
        parsed_data = load_yaml(data, Loader=Loader)
    return parsed_data



config = load_config()

bot = commands.Bot(command_prefix=config['prefix'])


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if (message.channel.is_news()):
        await message.publish()

@bot.command()
async def ping(ctx):
    await ctx.reply('Pong! `{}ms`'.format(floor(bot.latency * 1000)))

@bot.command()
async def invite(ctx):
    await ctx.reply(embed=Embed(color=0x03a5fc,title='Invite Bot', description='[**`[Invite Here]`**]({})'.format(config['invite_url'])))

@bot.command()
async def toggle_notifs(ctx):
    


@bot.event
async def on_ready():
    print('Ready!')

bot.run(config['token'])