import discord
from configs.con_config import settings


# Пишет сообщение вканал логов
async def sprintlog(bot, message: str):
    TCh: discord.channel = bot.get_channel(settings['home_guild_logs_channel'])
    await TCh.send('```[' + message + ']```')


# Пишет сообщение в канал логов, указывая автора команды
async def printlog(bot, author, message: str):
    TCh: discord.channel = bot.get_channel(settings['home_guild_logs_channel'])
    await TCh.send('```[команда: ' + author.name + '][' + message + ']```')
