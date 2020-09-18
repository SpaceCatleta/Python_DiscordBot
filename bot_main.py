import discord
from discord.ext import commands
from usersettings import params
from configs import config, con_config
from generallib import structs, textfile
from mycommands import simplecomm, dilogcomm, moderationcomm, systemcomm, datacommm, settingscomm, infocomm


# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
bot = commands.Bot(command_prefix=con_config.settings['prefix'])
guild: discord.Guild
UserStats = []


@bot.event
async def on_ready():
    global guild, UserStats
    guild = bot.get_guild(con_config.settings['home_guild_id'])
    readlist = textfile.ReadSymbolsStat(config.params['SymbolsStatisticsFile'])
    await params.init_dictinoraies()
    if len(readlist) == 0:
        for user in guild.members:
            UserStats.append(structs.userstats(user.id, 0))
    else:
        UserStats = readlist
    await dilogcomm.printlog(bot=bot, message='bot online')


@bot.event
async def on_message(mes: discord.Message):
    datacommm.stats_update(mes, UserStats)
    await bot.process_commands(message=mes)


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await datacommm.voice_stats_update(bot=bot, Stats_List=UserStats, member=member, before=before, after=after)


# Тестовое сообщение от бота
@bot.command()
async def tm(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await simplecomm.hello(ctx)


# Тестовоая команда
@bot.command()
async def test(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Показывает статистику указанного пользователя
@bot.command()
async def stats(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    emb_list = datacommm.user_stats_emb(ctx=ctx, StatsList=UserStats)
    emb = discord.Embed(color=discord.colour.Color.dark_magenta(),
                        title=emb_list[0], description=emb_list[1])
    await ctx.send(embed=emb)


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
async def commands_information(ctx: discord.ext.commands.Context):
    await ctx.send('```{0}```'.format(textfile.RadAll(config.params['info'])))


# Показать id текущего чата
@info.command(name='channelid')
async def find_channel_id(ctx: discord.ext.commands.Context):
    await ctx.send('```Channel id: {0}```'.format(ctx.channel.id))


# информация о сервере
@info.command(name='guild')
async def guild_information(ctx: discord.ext.commands.Context):
    await ctx.send('```{0}```'.format(infocomm.get_guild_information(ctx=ctx)))


# Информация дискорда о пользователе
@info.command(name='member')
async def member_information(ctx: discord.ext.commands.Context):
    await ctx.send('```{0}```'.format(infocomm.get_member_information(ctx=ctx)))


# ГРУППА


# Группа команд для модерации
@bot.group(nane='mod')
@commands.has_guild_permissions(manage_channels=True)
async def mod(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Утсанавливает роль для мута
@mod.command(name='moot')
async def give_moot(ctx: discord.ext.commands.Context):
    await moderationcomm.give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=params.accessparams['moot'])


# Утсанавливает роль для войс мута
@mod.command(name='voicemoot')
async def give_voice_moot(ctx: discord.ext.commands.Context):
    await moderationcomm.\
        give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=params.accessparams['voicemoot'])


# Утсанавливает роль с ограниченныи функциями
@mod.command(name='banfunc')
async def give_ban_func(ctx: discord.ext.commands.Context):
    await moderationcomm.\
        give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=params.accessparams['banfunc'])


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
async def set_ban_func_role(ctx: discord.ext.commands.Context):
    await settingscomm.set_Access_role(bot=bot, accessname='banfunc', ctx=ctx)


# Утсанавливает роль с ограниченныи функциями
@set.command(name='moot')
async def set_moot_role(ctx: discord.ext.commands.Context):
    await settingscomm.set_Access_role(bot=bot, accessname='moot', ctx=ctx)


# Утсанавливает роль с ограниченныи функциями
@set.command(name='voicemoot')
async def set_voice_moot_role(ctx: discord.ext.commands.Context):
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
    await dilogcomm.printlog(bot=bot, message='bot offline')
    await bot.close()


# Обращаемся к словарю settings с ключом token, для получения токена
print('boot bot...')
bot.run(con_config.settings['token'])
