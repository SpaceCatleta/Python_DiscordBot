import discord
from dateutil.tz import tzoffset
from datetime import datetime
from discord.ext import commands
from usersettings import params
from data import sqlitedb
from configs import config, con_config
from generallib import textfile, mainlib
from structs import userstats
from mycommands import simplecomm, dilogcomm, moderationcomm, datacommm, settingscomm, infocomm, dsVote


# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
bot = commands.Bot(command_prefix=con_config.settings['prefix'])
current_vote: dsVote.Vote = None
guild: discord.Guild
DB: sqlitedb.BotDataBase
settingslist = {}


@bot.event
async def on_ready():
    global guild, DB, settingslist
    DB = sqlitedb.BotDataBase('botdata.db')
    guild = bot.get_guild(con_config.settings['home_guild_id'])
    await params.init_dictinoraies()
    settingslist = DB.select_settings()
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
    await datacommm.voice_stats_update(bot=bot, DB=DB, member=member, before=before, after=after)


@bot.event
async def on_reaction_add(react: discord.Reaction, user):
    if current_vote is None:
        return
    current_vote.add_vote(emoji=react, user=user)


# Тестовое сообщение от бота
@bot.command()
async def tm(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await simplecomm.hello(ctx)


@bot.command(name='add_calc')
@commands.has_guild_permissions(administrator=True)
async def add_calc(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвал коанду -add_calc.'.format(ctx.message.author.name))
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
async def count(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвал коанду -count.'.format(ctx.message.author.name))
    await ctx.message.delete()
    counter: int = 0
    async for mes in ctx.channel.history(limit=10000, oldest_first=None):
        counter += 1
    await ctx.send('``` в данно канале {0} сообщений ```'.format(counter))


@bot.command()
async def calc(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -calc.'.format(ctx.message.author.name))
    await ctx.message.delete()
    newstat = await datacommm.calculate_txtchannel_stats(ctx.channel)
    answer = ''
    for stat in newstat:
        answer += '{0} напечатал {1} символов\n'.format(stat.name, stat.symb_counter)
    await ctx.send('```{0}```'.format(answer))


@bot.command()
@commands.has_guild_permissions(administrator=True)
async def calc_all(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -calc_all.'.format(ctx.message.author.name))
    await ctx.message.delete()
    g = ctx.author.guild
    new_stats = []
    counter: int = 0
    for channel in g.channels:
        if issubclass(type(channel), discord.TextChannel):
            counter += 1
            ch_stat = await datacommm.calculate_txtchannel_stats(channel)
            new_stats = datacommm.merge_stats(new_stats, ch_stat)
    answer = 'статистика из {0} каналов:\n'.format(counter)
    for stat in new_stats:
        answer += '{0} напечатал {1} символов\n'.format(stat.name, stat.symb_counter)
    await ctx.send('```{0}```'.format(answer))


@bot.command(name='print')
async def printer(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    print(str(ctx.message.content))


@bot.command(name='fixname')
async def fix_name(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -fixname.'.format(ctx.message.author.name))
    await ctx.message.delete()
    stat: userstats.userstats = DB.select(ctx.message.author.id)
    stat.name = ctx.message.author.name + '#' + str(ctx.message.author.discriminator)
    DB.update(stat=stat)


# Показывает статистику указанного пользователя
@bot.command()
async def stats(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -stats.'.format(ctx.message.author.name))
    await ctx.message.delete()
    emb_list = datacommm.user_stats_emb(ctx=ctx, DB=DB)
    emb = discord.Embed(color=discord.colour.Color.dark_magenta(),
                        title=emb_list[0], description=emb_list[1])
    await ctx.send(embed=emb)


# спам линком в чате
@bot.command()
async def bomb(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -bomb.'.format(ctx.message.author.name))
    for role in ctx.author.roles:
        if role.name == params.accessparams['banfunc']:
            return
    await ctx.message.delete()
    await simplecomm.bomb(ctx)


# Выдаёт информацию о коммандах
@bot.command(name='помощь')
async def userscom_information(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -помошь.'.format(ctx.message.author.name))
    await ctx.send('```{0}```'.format(textfile.RadAll(config.params['info'])))

# Выдаёт информацию о коммандах
@bot.command(name='moders')
@commands.has_guild_permissions(manage_channels=True)
async def userscom_information(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -moders.'.format(ctx.message.author.name))
    await ctx.send('```{0}```'.format(textfile.RadAll('data\info.txt') + '\n' + textfile.RadAll('data\info_moders.txt')))


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


@sys.command(name='recalc_stats')
async def sys_recalc_all(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -recalc_stats.'.format(ctx.message.author.name))
    global DB
    NewStats = []
    await dilogcomm.printlog(bot=bot,
        message='[команда: {0}]'.format(ctx.author.name) +
        await datacommm.calc_alltxtchannels_stats_after_time(guild=guild, time=None, DB=DB))
    for stat in NewStats:
        DB.update(stat)


# команда завершения работы
@sys.command(name='off')
async def sys_shutdown(ctx: discord.ext.commands.Context):
    params.shutdownparams['time'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
    textfile.WriteParams(params.shutdownparams, config.params['shutdown_info'], delsymb='=')
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='инициировано выключение.'.format(ctx.message.author.name))
    await dilogcomm.printlog(bot=bot, message='bot offline')
    await bot.close()


# Обращаемся к словарю settings с ключом token, для получения токена
print('boot')
bot.run(con_config.settings['token'])
