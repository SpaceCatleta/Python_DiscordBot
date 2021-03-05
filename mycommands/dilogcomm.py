import discord
import asyncio
from system import configs_obj
from configs.con_config import settings

gen_configs: configs_obj.GeneralConfig


# Пишет сообщение в канал логов, указывая автора команды
async def printlog(bot, message: str, params = None, **kwargs):
    log_mes = ''
    try:
        arg = kwargs['author']
        log_mes += '[команда: {0}]'.format(arg.name)
    except Exception:
        pass
    log_ch: discord.channel = bot.get_channel(settings['home_guild_logs_channel'])
    mes = '{0}[{1}]'.format(log_mes, message)

    if params is not None:
        mes += '\n\t<' + ', '.join([str(item) for item in params]) + '>'  # на случай, если params - кортеж
    await log_ch.send('```{0}```'.format(mes))


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

