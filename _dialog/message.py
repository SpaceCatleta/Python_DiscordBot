import discord
import asyncio
from configs.con_config import settings

from botdb.entities.GeneralSettings import GeneralSettings


generalSettings: GeneralSettings
bot: discord.Client

log_color = {'white': '',
             'red': 'diff\n-',
             'green': 'fix\n=',
             'yellow': 'fix\n'}


# Пишет сообщение в канал логов, указывая автора команды
async def log(message: str, color: str = 'white', params = None, ctx = None, **kwargs):
    log_mes = ''
    try:
        arg = kwargs['author']
        if ctx == None:
            log_mes += '[команда: {0}]'.format(arg.name)
        else:
            log_mes += '[{0}|{1}|{2}]'.format(ctx.guild.name, ctx.channel.name, ctx.author.name)
    except Exception:
        pass
    log_ch: discord.channel = bot.get_channel(settings['home_guild_logs_channel'])
    mes = '{0}[{1}]'.format(log_mes, message)

    if params is not None:
        mes += '\n\t<' + ', '.join([str(item) for item in params]) + '>'  # на случай, если params - кортеж
    await log_ch.send('```{0}\n{1}```'.format(log_color[color], mes))


# Отправляет временное сообщение (отправляется по контексту)
async def bomb_message(ctx, message: str, type: str = 'standard'):
    color = None

    if type == 'standard':
        color = discord.colour.Colour.orange()
    elif type == 'error':
        color = discord.colour.Colour.red()
    elif type == 'success':
        color = discord.colour.Colour.green()

    emb: discord.Embed = discord.Embed(color=color, description=message)
    mes = await ctx.send(embed=emb)
    await asyncio.sleep(generalSettings.bombMessagesTime)
    await mes.delete()


# Отправляет временное сообщение (отправляется по сообщеню)
async def bomb_message2(mes, text: str, type: str = 'standard'):
    color = None

    if type == 'standard':
        color = discord.colour.Colour.orange()
    elif type == 'error':
        color = discord.colour.Colour.red()
    elif type == 'success':
        color = discord.colour.Colour.green()

    emb: discord.Embed = discord.Embed(color=color, description=text)
    mes = await mes.channel.send(embed=emb)
    await asyncio.sleep(generalSettings.bombMessagesTime)
    await mes.delete()