import discord
import time
from discord.ext import commands
from usersettings import params
from configs import config, con_config
from generallib import mainlib, structs, textfile as TFile
from mycommands import simplecomm, dilogcomm, moderationcomm, systemcomm, datacommm, settingscomm


# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
bot = commands.Bot(command_prefix=con_config.settings['prefix'])
guild: discord.Guild
UserStats = []


@bot.event
async def on_ready():
    global guild, UserStats
    guild = bot.get_guild(con_config.settings['home_guild_id'])
    readlist = TFile.ReadSymbolsStat(config.params['SymbolsStatisticsFile'])
    await params.init_dictinoraies()
    if len(readlist) == 0:
        for user in guild.members:
            UserStats.append(structs.userstats(user.id, 0))
    else:
        UserStats = readlist
    TCh: discord.channel = bot.get_channel(con_config.settings['home_guild_logs_channel'])
    await TCh.send('```[bot online]```')


@bot.event
async def on_message(mes: discord.Message):
    datacommm.stats_update(mes, UserStats)
    await bot.process_commands(mes)

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None:
        user = structs.searchid(list=UserStats, ID=member.id)
        user.connect_time = time.time()
    if after.channel is None:
        user = structs.searchid(list=UserStats, ID=member.id)
        user.name = member.name
        chat_time = time.time() - user.connect_time
        if chat_time > 10000000:
            await dilogcomm.sprintlog(bot=bot, message='{0} - ошибка вычисления в гс чате [{1}]'.format(user.name,
                                                                                                        chat_time))
        else:
            user.vc_counter += chat_time
            await dilogcomm.sprintlog(bot=bot, message='{0} пробыл в гс {1}сек.'.format(user.name, chat_time))


# Тестовое сообщение от бота
@bot.command()
async def tm(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await simplecomm.hello(ctx)


@bot.command()
async def mestext(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    async for m in ctx.channel.history(limit=1):
        await ctx.send(str(m.content))


# Тестовоая команда
@bot.command()
async def test(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    i = 0
    async for m in ctx.channel.history(limit=10000):
        i += 1
    await ctx.send('```в данном канале {0} сообщений```'.format(str(i)))


# Показывает статистику указанного пользователя
@bot.command()
async def stats(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await ctx.send('```{0}```'.format(datacommm.userstats(ctx=ctx, StatsList=UserStats)))


# спам линком в чате
@bot.command()
async def bomb(ctx: discord.ext.commands.Context):
    for role in ctx.author.roles:
        if role.name == params.accessparams['banfunc']:
            return
    await ctx.message.delete()
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


# Утсанавливает роль для мута
@mod.command(name='moot')
async def give_moot(ctx: discord.ext.commands.Context):
    await moderationcomm.give_timer_role(bot=bot,ctx=ctx,RoleList=guild.roles,rolename=params.accessparams['moot'])


# Утсанавливает роль для войс мута
@mod.command(name='voicemoot')
async def give_voicemoot(ctx: discord.ext.commands.Context):
    await moderationcomm.give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=params.accessparams['voicemoot'])


# Утсанавливает роль с ограниченныи функциями
@mod.command(name='banfunc')
async def give_banfunc(ctx: discord.ext.commands.Context):
    await moderationcomm.give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=params.accessparams['banfunc'])


# Удаление сообщений
@mod.command(name='clearmes')
async def clearmes(ctx: discord.ext.commands.Context):
    await moderationcomm.deletemessages(bot, ctx=ctx, stats=UserStats)


# ГРУППА


# Группа коанд для настроек
@bot.group(nane='set')
@commands.has_guild_permissions(manage_channels=True)
async def set(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Утсанавливает роль с ограниченныи функциями
@set.command(name='banfunc')
async def set_banfunc_role(ctx: discord.ext.commands.Context):
    await settingscomm.set_Access_role(bot=bot, accessname='banfunc', ctx=ctx)


# Утсанавливает роль с ограниченныи функциями
@set.command(name='moot')
async def set_moot_role(ctx: discord.ext.commands.Context):
    await settingscomm.set_Access_role(bot=bot, accessname='moot', ctx=ctx)


# Утсанавливает роль с ограниченныи функциями
@set.command(name='voicemoot')
async def set_voicemoot_role(ctx: discord.ext.commands.Context):
    await settingscomm.set_Access_role(bot=bot, accessname='voicemoot', ctx=ctx)


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
