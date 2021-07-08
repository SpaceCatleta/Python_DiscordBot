import discord
import asyncio
from system import configs_obj
from configs.con_config import settings

gen_configs: configs_obj.GeneralConfig

log_color = {'white': '',
             'red': 'diff\n-',
             'green': 'fix\n='}


# Пишет сообщение в канал логов, указывая автора команды
async def printlog(bot, message: str, color: str = 'white', params = None, ctx = None, **kwargs):
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
    await log_ch.send('```{0}{1}```'.format(log_color[color], mes))


# Отправляет временное сообщение
async def bomb_message(ctx, message: str, type: str = 'standard'):

    color = None
    title = 'None'
    if type == 'standard':
        color = discord.colour.Colour.orange()
        title = 'Системное сообщение'
    elif type == 'error':
        color = discord.colour.Colour.red()
        title = 'Ошибка'

    emb: discord.Embed = discord.Embed(color=color, description=message)
    mes = await ctx.send(embed=emb)
    await asyncio.sleep(gen_configs.bomb_mes_time)
    await mes.delete()

