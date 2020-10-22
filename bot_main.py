import discord
from dateutil.tz import tzoffset
from datetime import datetime
from discord.ext import commands
from usersettings import params
from data import sqlitedb
from configs import config, con_config
from generallib import textfile, mainlib
from structs import userstats, userstatslist
from mycommands import simplecomm, dilogcomm, moderationcomm, datacommm, settingscomm, infocomm, dsVote


# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
bot = commands.Bot(command_prefix=con_config.settings['prefix'])
current_vote: dsVote.Vote = None
guild: discord.Guild
DB: sqlitedb.BotDataBase
ProcessingUsers: userstatslist.UserStatsList
settingslist = {}
shortstart: bool = True

@bot.event
async def on_ready():
    global guild, DB, settingslist, ProcessingUsers
    ProcessingUsers = userstatslist.UserStatsList()
    DB = sqlitedb.BotDataBase('botdata.db')
    guild = bot.get_guild(con_config.settings['home_guild_id'])
    await params.init_dictinoraies()
    settingslist = DB.select_settings()
    if shortstart:
        await dilogcomm.printlog(bot=bot, message='bot online')
        return
    await dilogcomm.printlog(bot=bot,
                             message='обнаружено время последней записи: {0}'.format(params.shutdownparams['time']))
    time: datetime = datetime.strptime(params.shutdownparams['time'], "%Y-%m-%d %H:%M:%S")
    n = 4
    time.astimezone(tzoffset("UTC+{}".format(n), n * 60 * 60))
    await dilogcomm.printlog(bot=bot,
        message=await datacommm.calc_alltxtchannels_stats_after_time(guild=guild, time=time, DB=DB))
    await dilogcomm.printlog(bot=bot, message='bot online')


@bot.event
async def on_message(mes: discord.Message):
    datacommm.stats_update(mes=mes, DB=DB)
    await bot.process_commands(message=mes)


@bot.event
async def on_member_join(member):
    DB.insert(userstats.userstats(ID=member.id, Name=member.name))
    await member.add_roles(mainlib.Findrole(rolelist=guild.roles, serchrole=settingslist['base_role']))


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await datacommm.voice_stats_update(bot=bot, DB=DB, Processing=ProcessingUsers,
                                       member=member, before=before, after=after)


@bot.event
async def on_reaction_add(react: discord.Reaction, user):
    if current_vote is None:
        return
    current_vote.add_vote(emoji=react, user=user)


# Тестовое сообщение от бота
@bot.command()
async def tm(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    emb: discord.Embed = discord.Embed(title='ваш аватар')
    emb.set_author(name='user', url=ctx.author.avatar_url)
    emb.set_thumbnail(url=ctx.author.avatar_url)
    emb.add_field(name='field1:', value='value1')
    emb.add_field(name='field2:', value='value2')
    emb.add_field(name='field3:', value='value3', inline=False)
    await ctx.send(embed=emb)
    # await simplecomm.hello(ctx)


@bot.command(name='add_calc')
@commands.has_guild_permissions(administrator=True)
async def add_calc(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвал коанду -add_calc'.format(ctx.message.author.name))
    await ctx.message.delete()
    time: datetime = datetime.strptime(params.shutdownparams['time'], "%Y-%m-%d %H:%M:%S")
    n = 4
    time.astimezone(tzoffset("UTC+{}".format(n), n*60*60))
    counter: int = 0
    async for message in ctx.channel.history(limit=100, after=time):
        counter += 1
    await ctx.send(str(counter))


@bot.command()
async def channels(ctx: discord.ext.commands.Context):
    g = ctx.author.guild
    answer: str = str(len(g.channels)) + '\n'
    for channel in g.channels:
        answer += channel.name + '\n'
    await ctx.send(answer)


@bot.command()
async def txtchannels(ctx: discord.ext.commands.Context):
    g = ctx.author.guild
    counter: int = 0
    answer: str = ''
    for channel in g.channels:
        if issubclass(type(channel), discord.TextChannel):
            answer += channel.name + '\n'
            counter += 1
    answer = str(counter) + '\n' + answer

    await ctx.send(answer)


# Начинает голосование
@bot.command(name='vote')
async def boot_vote(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='запущено голосование'.format(ctx.message.author.name))
    await ctx.message.delete()
    global current_vote
    if current_vote is not None:
        await ctx.send('```Одно голосование уже ведётся, дождитесь его завершения, чтобы начать новое```')
        return
    current_vote = dsVote.create_vote(bot=bot, ctx=ctx)
    await current_vote.show()
    del current_vote
    current_vote = None


@bot.command()
async def calc(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -calc'.format(ctx.message.author.name))
    await ctx.message.delete()
    newstat: userstatslist.UserStatsList = await datacommm.calculate_txtchannel_stats(ctx.channel)
    answer = ''
    for stat in newstat:
        answer += '{0} напечатал {1} символов\n'.format(stat.name, stat.symb_counter)
    await ctx.send('```{0}```'.format(answer))


@bot.command()
@commands.has_guild_permissions(administrator=True)
async def calc_all(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -calc_all'.format(ctx.message.author.name))
    await ctx.message.delete()
    await ctx.send('```{0}```'.format(await datacommm.print_all_txtchannel_stats(ctx=ctx)))


@bot.command(name='print')
async def printer(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    print(str(ctx.message.content))


@bot.command(name='fixname')
async def fix_name(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -fixname'.format(ctx.message.author.name))
    await ctx.message.delete()
    stat: userstats.userstats = DB.select(ctx.message.author.id)
    stat.name = ctx.message.author.name + '#' + str(ctx.message.author.discriminator)
    DB.update(stat=stat)


@bot.command(name='stats')
async def stats(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -stats'.format(ctx.message.author.name))
    await ctx.message.delete()
    await ctx.send(embed=datacommm.user_stats_emb(ctx=ctx, DB=DB))


# Показывает статистику указанного пользователя
@bot.command(name='stats_old')
async def stats2(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -stats_old'.format(ctx.message.author.name))
    await ctx.message.delete()
    await ctx.send(embed=datacommm.user_stats_emb2(ctx=ctx, DB=DB))


# проверка, находится ли пользователь в сети
@bot.command(name='online')
async def is_online(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -online'.format(ctx.message.author.name))
    await ctx.message.delete()
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    if user.status != discord.Status.offline:
        await ctx.send('пользователь {0} сейчас в сети'.format(user.name))
    else:
        await ctx.send('пользователь {0} сейчас не в сети'.format(user.name))


# спам линком в чате
@bot.command()
async def bomb(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -bomb'.format(ctx.message.author.name))
    for role in ctx.author.roles:
        if role.name == params.accessparams['banfunc']:
            return
    await ctx.message.delete()
    await simplecomm.bomb(ctx)


# Выдаёт информацию о коммандах
@bot.command(name='помощь')
async def userscom_information(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -помошь'.format(ctx.message.author.name))
    await ctx.send('```{0}```'.format(textfile.RadAll(config.params['info'])))


# Выдаёт информацию о коммандах
@bot.command(name='moders')
@commands.has_guild_permissions(manage_channels=True)
async def userscom_information(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -moders'.format(ctx.message.author.name))
    await ctx.send('```{0}```'.format(textfile.RadAll('data\info.txt') +
                                      '\n' + textfile.RadAll('data\info_moders.txt')))


# ГРУППА


# Группа информационных команд
@bot.group(nane='info')
async def info(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


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


# Информация о кол-ве сообщений в канале
@info.command()
async def count(ctx: discord.ext.commands.Context):
    await ctx.send('```{0}```'.format(await infocomm.count_channel_messages(bot=bot, ctx=ctx)))


# ГРУППА


# Группа команд для модерации
@bot.group(nane='mod')
@commands.has_guild_permissions(manage_channels=True)
async def mod(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Утсанавливает роль для мута
@mod.command(name='moot')
async def give_moot(ctx: discord.ext.commands.Context):
    await moderationcomm.give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=settingslist['moot'])


# Утсанавливает роль для войс мута
@mod.command(name='voicemoot')
async def give_voice_moot(ctx: discord.ext.commands.Context):
    await moderationcomm.\
        give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=settingslist['vc_moot'])


# Утсанавливает роль с ограниченныи функциями
@mod.command(name='banfunc')
async def give_ban_func(ctx: discord.ext.commands.Context):
    await moderationcomm.\
        give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=settingslist['ban_functions'])


# Удаление сообщений
@mod.command(name='clearmes')
async def clearmes(ctx: discord.ext.commands.Context):
    await moderationcomm.deletemessages(bot, ctx=ctx, DB=DB)


# ГРУППА


# Группа коанд для настроек
@bot.group(nane='set')
@commands.has_guild_permissions(manage_channels=True)
async def set(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Утсанавливает роль с ограниченныи функциями
@set.command(name='banfunc')
async def set_ban_func_role(ctx: discord.ext.commands.Context):
    await settingscomm.set_Access_role(bot=bot, DB=DB, accessname='ban_functions', ctx=ctx)


# Утсанавливает роль с ограниченныи функциями
@set.command(name='moot')
async def set_moot_role(ctx: discord.ext.commands.Context):
    await settingscomm.set_Access_role(bot=bot, DB=DB, accessname='moot', ctx=ctx)


# Утсанавливает роль с ограниченныи функциями
@set.command(name='vcmoot')
async def set_voice_moot_role(ctx: discord.ext.commands.Context):
    await settingscomm.set_Access_role(bot=bot, DB=DB, accessname='vc_moot', ctx=ctx)


# Утсанавливает роль с ограниченныи функциями
@set.command(name='baserole')
async def set_base_role(ctx: discord.ext.commands.Context):
    await settingscomm.set_Access_role(bot=bot, DB=DB, accessname='base_role', ctx=ctx)


# ГРУППА


# Группа систеных комманд
@bot.group(nane='sys')
@commands.has_guild_permissions(manage_channels=True)
async def sys(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Перерассчитывает статистику по сообщениям на сервере
@sys.command(name='recalc_stats')
@commands.has_guild_permissions(administrator=True)
async def sys_recalc_all(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -recalc_stats'.format(ctx.message.author.name))
    global DB
    g = ctx.author.guild
    new_stats: await datacommm.calculate_all_txtchannel_stats(ctx=ctx)
    old_stat: userstats.userstats
    for stat in new_stats:
        old_stat = DB.select(stat.id)
        if old_stat is None:
            DB.insert(stat)
        elif old_stat.symb_counter < stat.symb_counter:
            old_stat.clear(vc_clear=False)
            old_stat.add(stat)
            old_stat.calculate_exp()
            DB.update(old_stat)
    answer = 'произведён перерасчёт статистики\nстатистика из всех каналов:\n'
    for stat in new_stats:
        answer += '{0} напечатал {1} символов\n'.format(stat.name, stat.symb_counter)
    await dilogcomm.printlog(bot=bot, message=answer)


# Перерассчитывает опыт и перезаписывает имена всех пользователей
@sys.command(name='fixstats')
async def fixstats(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -fixstats'.format(ctx.message.author.name))
    global DB
    g = ctx.author.guild
    stats: userstats.userstats
    for member in ctx.author.guild.members:
        stats = DB.select(member.id)
        if stats is None:
            DB.insert(userstats.userstats(ID=member.id, Name=member.name))
        else:
            stats.calculate_exp()
            stats.name = member.name
            DB.update(stat=stats)
    await dilogcomm.printlog(bot=bot,
                             message='статистика опыта и имена пользователей обновлены'.format(ctx.message.author.name))


# команда завершения работы
@sys.command(name='off')
async def sys_shutdown(ctx: discord.ext.commands.Context):
    params.shutdownparams['time'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
    textfile.WriteParams(params.shutdownparams, config.params['shutdown_info'], delsymb='=')
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='инициировано выключение'.format(ctx.message.author.name))
    await dilogcomm.printlog(bot=bot, message='bot offline')
    await bot.close()


# Обращаемся к словарю settings с ключом token, для получения токена
print('boot')
bot.run(con_config.settings['token'])
