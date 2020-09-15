import discord
from discord.ext import commands
from configs import config, con_config
from generallib import mainlib, structs, textfile as TFile
from mycommands import simplecomm, dilogcomm, moderationcomm, systemcomm, datacommm


# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
bot = commands.Bot(command_prefix=con_config.settings['prefix'])
guild: discord.Guild
UserStats = []


@bot.event
async def on_ready():
    global guild, UserStats
    guild = bot.get_guild(con_config.settings['home_guild_id'])
    readlist = TFile.ReadSymbolsStat(config.params['SymbolsStatisticsFile'])
    if len(readlist) == 0:
        for user in guild.members:
            UserStats.append(structs.userstats(user.id, 0))
    else:
        UserStats = readlist
    TCh: discord.channel = bot.get_channel(con_config.settings['home_guild_logs_channel'])
    await TCh.send('```[bot online]```')


@bot.event
async def on_message(mes: discord.Message):
    if mes.author.bot:
        return
    global UserStats
    stat: structs.userstats = structs.searchid(UserStats, mes.author.id)
    if stat is not None:
        stat.counter += mainlib.mylen(mes.content)
    else:
        UserStats.append(structs.userstats(ID=mes.author.id, Counter=mainlib.mylen(mes.content)))
    await bot.process_commands(mes)


# Тестовое сообщение от бота
@bot.command()
async def tm(ctx: discord.ext.commands.Context, **kwargs):
    await ctx.message.delete()
    await simplecomm.hello(ctx)


# Показывает статистику указанного пользователя
@bot.command()
async def stats(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await ctx.send('```' + await datacommm.userstats(ctx=ctx, StatsList=UserStats) + '```')


# спам линком в чате
@bot.command()
async def bomb(ctx: discord.ext.commands.Context):
    for role in ctx.author.roles:
        if role.name == 'шиза':
            return
    await simplecomm.bomb(ctx)


# ГРУППА


# Группа информационных команд
@bot.group(nane='info')
async def info(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Выдаёт информацию о коммандах
@info.command(name='commands')
async def commands_information(ctx: discord.ext.commands.Context, **kwargs):
    await ctx.send('```' + TFile.RadAll(config.params['info']) + '```')


# Показать id текущего чата
@info.command(name='channelid')
async def find_channelid(ctx: discord.ext.commands.Context):
    await ctx.send('```Channel id: ' + str(ctx.channel.id) + '```')


# информация о сервере
@bot.command(name='guild')
async def guild_information(ctx: discord.ext.commands.Context):
    answer = 'Название сервера: ' + ctx.author.guild.name + '\n'
    answer += 'ID сервера: ' + str(ctx.author.guild.id) + '\n'
    answer += 'Количество участников: ' + str(ctx.author.guild.member_count) + '\nучастники:\n'
    for user in ctx.author.guild.members:
        answer += user.name + ' [' + str(user.nick) + ']\n'
    await ctx.send('```' + answer + '```')


# Информация дискорда о пользователе
@bot.command(name='member')
async def member_information(ctx: discord.ext.commands.Context):
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    await ctx.message.delete()
    answer = 'Основной ник: ' + user.name + '#' + user.discriminator + '\n'
    answer += 'Ник на сервере: ' + user.display_name + '\n'
    answer += 'ID: ' + str(user.id) + '\n'
    answer += 'Бот: ' + ('да' if user.bot else 'нет') + '\n'
    answer += 'Вступил: ' + str(user.joined_at) + '\n'
    await ctx.send('```' + answer + '```')


# ГРУППА


# Группа команд для модерации
@bot.group(nane='mod')
@commands.has_guild_permissions(manage_channels=True)
async def mod(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Удаление сообщений
@mod.command(name='clearmes')
async def clearmes(ctx: discord.ext.commands.Context):
    await moderationcomm.deletemessages(bot, ctx=ctx, stats=UserStats)


# Урезание статистики указанного пользователя
@mod.command(name='-stats')
async def down_stats(ctx: discord.ext.commands.Context):
    await datacommm.ChangeSymbStats(bot=bot, ctx=ctx, StatsList=UserStats)


# ГРУППА


# Группа систеных комманд
@bot.group(nane='sys')
@commands.has_guild_permissions(manage_channels=True)
async def sys(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Запись данных в файл
@sys.command(name='write')
async def write_txt(ctx: discord.ext.commands.Context):
    await systemcomm.writestats(bot=bot, UserStats=UserStats)


# команда завершения работы
@sys.command(name='off')
async def sys_shutdown(ctx: discord.ext.commands.Context):
    await systemcomm.writestats(bot=bot, UserStats=UserStats)
    await dilogcomm.sprintlog(bot=bot, message='bot offline')
    await bot.close()


# Обращаемся к словарю settings с ключом token, для получения токена
print('boot bot...')
bot.run(con_config.settings['token'])
