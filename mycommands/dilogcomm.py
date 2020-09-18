import discord
from configs.con_config import settings


# Пишет сообщение в канал логов, указывая автора команды
async def printlog(bot, message: str, **kwargs):
    log_mes = ''
    try:
        arg = kwargs['author']
        log_mes += '[команда: {0}]'.format(arg.name)
    except Exception:
        pass
    log_ch: discord.channel = bot.get_channel(settings['home_guild_logs_channel'])
    await log_ch.send('```{0}[{1}]```'.format(log_mes, message))
