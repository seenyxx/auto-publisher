from nextcord.embeds import Embed
from nextcord.ext import commands
from yaml import load as load_yaml, Loader
from math import floor
import pickledb

db = pickledb.load('data.db', True)

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

    if (not message.guild):
        return
    if (not message.guild.me.guild_permissions.administrator):
        return
    
    if (message.author.id == message.guild.me.id or message.author.bot):
        return

    if (message.content.startswith(config['prefix'])):
        return

    if (message.channel.is_news()):
        db_key = 'notifs_{}'.format(message.author.id)

        if (db.exists(db_key)):
            if (not message.author.dm_channel):
                await message.author.create_dm()
            await message.author.dm_channel.send('Published your message in <{}>'.format('#' + str(message.channel.id)))
            
        await message.publish()

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def ping(ctx):
    await ctx.reply('Pong! `{}ms`'.format(floor(bot.latency * 1000)))

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def invite(ctx):
    await ctx.reply(embed=Embed(color=0x03a5fc,title='Invite Bot', description='[**`[Invite Here]`**]({})'.format(config['invite_url'])))

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name='toggle-notifs')
async def toggle_notifs(ctx):
    user = ctx.author.id
    db_key = 'notifs_{}'.format(user)
    current_val = db.exists(db_key)

    if (not current_val):
        await ctx.reply('DM notifications set to True 🟩')
        db.set(db_key, True)
    else:
        await ctx.reply('DM notifications set to False 🟥')
        db.rem(db_key)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(title='You cannot use this command yet! ⌚',description='Try again in **{:.2f} seconds**'.format(error.retry_after), color=0x001b3b)
        await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print('Ready!')

bot.run(config['token'])