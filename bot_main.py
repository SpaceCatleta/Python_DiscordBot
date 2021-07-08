import discord, asyncio, re
from system import configs_obj
from processing import roles_proc, messages_proc
from dateutil.tz import tzoffset
from datetime import datetime
from discord.ext import commands
from usersettings import params
from data import sqlitedb
from configs import config, con_config, runtime_settings
from generallib import textfile
from structs import userstats, userstatslist
from mycommands import simplecomm, dilogcomm, moderationcomm, datacommm, infocomm, dsVote
from functions import gif_triggers
from functions import simple
from information import _shortcut


# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=con_config.settings['prefix'], intents=intents)
# текущее голосование
current_vote: dsVote.Vote = None
# текущая гильдия
guild: discord.Guild
# объект-обёртка для взаимодействия с базой данных
DB: sqlitedb.BotDataBase
ProcessingUsers: userstatslist.UserStatsList
# метка для быстрого пуска (для проведения тестов)
short_start: bool = True
# список id пользователей, чьи команды уже выполняются.
exe_list = []
# хранит системные настройки и обеспечивает работу с файлом настроек
gen_configs: configs_obj.GeneralConfig
# хранит настройки ролей и обеспечивает работу с файлом настроек
roles_configs: configs_obj.RolesConfig
# запущен ли бот
sys_boot : bool = False

is_crashed: bool = False
is_calculating: bool = False
timeouts: int = 0



# ======================================================================================================================
# ===== СОБЫТИЯ =====
# ======================================================================================================================

# события при включении бота
@bot.event
async def on_ready():
    global guild, DB, ProcessingUsers, gen_configs, roles_configs, bot
    runtime_settings.bot = bot
    ProcessingUsers = userstatslist.UserStatsList()
    DB = sqlitedb.BotDataBase('botdata.db')
    gif_triggers.init(path='functions/gif_triggers.db')
    guild = bot.get_guild(con_config.settings['home_guild_id'])
    gen_configs = configs_obj.GeneralConfig()
    dilogcomm.gen_configs = gen_configs
    roles_configs = configs_obj.RolesConfig()
    await params.init_dictinoraies()
    if short_start:
        await dilogcomm.printlog(bot=bot, message='bot online')
        return
    # дорассчёт статистики
    await dilogcomm.printlog(bot=bot,
                             message='обнаружено время последней записи: {0}'.format(params.shutdownparams['time']))
    time: datetime = datetime.strptime(params.shutdownparams['time'], "%Y-%m-%d %H:%M:%S")
    n = 4
    time.astimezone(tzoffset("UTC+{}".format(n), n * 60 * 60))
    await dilogcomm.printlog(bot=bot,
        message=await datacommm.calc_alltxtchannels_stats_after_time(guild=guild, time=time, DB=DB))
    await update_write_time()
    await dilogcomm.printlog(bot=bot, message=params.shutdownparams['time'])
    await update_data_loop()
    await dilogcomm.printlog(bot=bot, message='bot online')


@bot.event
async def on_message(mes: discord.Message):
    link_count = messages_proc.symbols_in_text(mes.content, '@')
    if link_count > gen_configs.max_links:
        await mes.delete()
        await mes.channel.send('```удалено сообщение с недопустимым количеством упоминаний```')
        log = 'канал: {0}, пользователь: {1}][удалено сообщение с недопустимым количеством упоминаний'.\
            format(mes.author.name, mes.channel.name)
        await dilogcomm.printlog(bot=bot, message=log)
        return
    datacommm.stats_update(mes=mes, DB=DB)
    try:
        await asyncio.wait_for(bot.process_commands(message=mes), timeout=gen_configs.timeout)
    except asyncio.TimeoutError:
        await mes.channel.send('```timeout```')


@bot.event
async def on_member_join(member):
    await dilogcomm.printlog(bot=bot, message="пользователь {0} зашёл на сервер {1}".
                             format(member.display_name, member.guild.nane), color='green')
    embed = discord.Embed(colour=discord.colour.Color.green())
    embed.description = "Пользователь {0} присоединился к нам".format(member.display_name)
    await member.guild.system_channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    await dilogcomm.printlog(bot=bot, message="пользователь {0} покинул сервер {1}".
                             format(member.display_name, member.guild.nane), color='red')
    embed = discord.Embed(colour=discord.colour.Color.red())
    embed.description = "Пользователь {0} покинул нас".format(member.display_name)
    await member.guild.system_channel.send(embed=embed)


@bot.event
async def on_member_ban(guild, user):
    await dilogcomm.printlog(bot=bot, message="пользователь {0} был забанен на сервере {1}".
                             format(user.name, guild.name), color='red')
    embed = discord.Embed(colour=discord.colour.Color.red())
    embed.description = "Пользователь {0} был забанен".format(user.name)
    await guild.system_channel.send(embed=embed)


@bot.event
async def on_member_unban(guild, user):
    await dilogcomm.printlog(bot=bot, message="пользователь {0} был разбанен на сервере {1}".
                             format(user.name, guild.name), color='green')


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await datacommm.voice_stats_update(bot=bot, DB=DB, Processing=ProcessingUsers,
                                       member=member, before=before, after=after)


@bot.event
async def on_reaction_add(react: discord.Reaction, user):
    if current_vote is None:
        return
    current_vote.add_vote(emoji=react, user=user)


# ======================================================================================================================
# ===== СИСТЕМНЫЕ ФУНКЦИИ =====
# ======================================================================================================================


# Выполнение команды со всеми проверками
async def correct_boot(fun, ctx, is_high_prior: bool = False, is_calc_func: bool = False, *words):
    global is_calculating, is_crashed
    if not is_high_prior:
        if is_crashed:
            print('выполнение комманд временно заблокированно')
            return
        elif is_calculating:
            print('выполняются вычисления')
            return

    await ctx.message.delete()
    func_name = str(fun).split(' ')[1]
    author = ctx.message.author
    await dilogcomm.printlog(bot=bot, author=author,
                             message='вызвана функция -{0}'.format(func_name),
                             params=words)

    is_calculating = True if is_calc_func else is_calculating
    try:
        if await fun(ctx, words) == -2:       # <------------------------------ Вызов функции тут
            await dilogcomm.printlog(bot=bot, author=author,
                                     message='выполнение функции {0} прервано'.format(func_name))
    except asyncio.TimeoutError:
        is_calculating = False if is_calc_func else is_calculating
        await timeout_check()
    is_calculating = False if is_calc_func else is_calculating


# Отслеживание таймаутов
async def timeout_check():
    global timeouts, is_crashed
    timeouts += 1
    if timeouts >= gen_configs.timeout_limit:
        is_crashed = True
        timeouts = 0
        await dilogcomm.printlog(bot=bot, message='произошла перегрузка, функции заблокированны на {0}с.'.
                                 format(gen_configs.timeout))
        await asyncio.sleep(gen_configs.timeout)
        is_crashed = False


# Проверка корректного вызова
@bot.command()
async def test(ctx: discord.ext.commands.Context, *words):
    await correct_boot(tf, ctx, False, False, words)

@bot.command()
async def tf(ctx, *words):
    text = '12 *3* 123'
    await ctx.send(text)


# Тест системных собщений
@bot.command()
async def stest(ctx: discord.ext.commands.Context):
    await dilogcomm.bomb_message(ctx=ctx, message='test')


@bot.command()
async def find_id(ctx: discord.ext.commands.Context, *words):
    await ctx.message.delete()
    await  dilogcomm.printlog(bot=bot, author=ctx.author, message='find_id', params=words)
    user = await bot.fetch_user(int(words[0]))
    await ctx.send('```id: {0}\nuser: {1}```'.format(words[0], user))

# ======================================================================================================================
# ===== КОМАНДЫ =====
# ======================================================================================================================


# Команда транслита с английской раскладки
@bot.command(name='р')
async def change_keyword(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -р')
    answer = await simple.find_and_change_keys(ctx=ctx)
    if answer == -1:
        await dilogcomm.bomb_message(ctx=ctx, message='сообщение пользователя не найдено среди 10 последних')
    else:
        await ctx.send(answer)


# Команда триггеров
@bot.command()
async def t(ctx: discord.ext.commands.Context, *words):
    await ctx.message.delete()

    """-t [комманда] [ключевое слово] [параметры]"""
    if words[0] == 'help':          # ===== ПОМОЩЬ
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t help', ctx=ctx)
        await ctx.send(textfile.RadAll('information/triggers_help.txt'))

    elif words[0] == 'list':        # ===== ЗАПРОС ДАННЫХ О ВСЁМ СПИСКЕ
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t list', ctx=ctx)
        await ctx.send('```' + gif_triggers.get_trigger_list() + '```')

    elif words[0] == 'lock':        # ===== СМЕНА РЕЖИМА ДОСТУПА
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t lock', params=words[1:], ctx=ctx)
        if gif_triggers.switch_lock(words[1]) == -1:
            await dilogcomm.bomb_message(ctx=ctx, message='неверное ключевое слово', type='error')
        else:
            await dilogcomm.bomb_message(ctx=ctx, message='доступ к триггеру {0} изменён'.format(words[1]))

    elif words[0] == 'edit':        # ===== СМЕНА ФРАЗЫ ТРИГГЕРА
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t edit',params=words[1:], ctx=ctx)
        if gif_triggers.update_trigger_discr(name=words[1], new_discr=' '.join(words[2:])) == -1:
            await dilogcomm.bomb_message(ctx=ctx, message='неверное ключевое слово', type='error')
        else:
            await dilogcomm.bomb_message(ctx=ctx, message='фраза у триггера {0} изменена'.format(words[1]))

    elif words[0] == 'info':        # ===== ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ТРИГГЕРЕ
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t info', ctx=ctx)
        ans = await gif_triggers.get_trigger_info(name=words[1], bot=bot)
        if ans == -1:
            await dilogcomm.bomb_message(ctx=ctx, message='неверное ключевое слово', type='error')
        else:
            await ctx.send('```' + ans + '```')

    elif words[0] == 'delete':      # ===== УДАЛЕНИЕ
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t delete', params=words[1:], ctx=ctx)
        if gif_triggers.delete_trigger(name=words[1]) == -1:
            await dilogcomm.bomb_message(ctx=ctx, message='неверное ключевое слово', type='error')
        else:
            await dilogcomm.bomb_message(ctx=ctx, message='триггер {0} удалён'.format(words[1]))

    elif words[0] == 'new':         # ===== ДОБАВЛЕНИЕ НОВОГО КЛЮЧЕВОГО СЛОВА
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t new', params=words[1:], ctx=ctx)
        if len(words) > 2:
            ans = gif_triggers.add_new_trigger(ctx.author.id, words[1].replace('_', ' ').lower(), ' '.join(words[2:]))
        else:
            ans = gif_triggers.add_new_trigger(ctx.author.id, words[1].replace('_', ' ').lower())
        if ans == 0:
            await dilogcomm.bomb_message(ctx=ctx, message='<{0}> создано'.format(words[1].replace('_', ' ')))
        else:
            await dilogcomm.bomb_message(ctx=ctx, message='данный триггер уже создан', type='error')

    elif words[0] == 'add':         # ===== ДОБАВЛЕНИЕ GIF
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t add', params=words[1:], ctx=ctx)
        URL_mes = await search_gif_mes(ctx=ctx)
        if URL_mes == None:
            await dilogcomm.bomb_message(ctx=ctx, message='в последних 10 сообщениях gif не обнаружены')
        else:
            answer = gif_triggers.add_new_gif(user_id=ctx.author.id, name=words[1], url=str(URL_mes))
            if answer == 0:
                await dilogcomm.bomb_message(ctx=ctx, message='gif добалвена в {0}'.format(words[1]))
            else:
                await dilogcomm.bomb_message(ctx=ctx, message=answer, type='error')

    elif words[0] == 'remove':      # ===== УДАЛЕНИЕ GIF
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t remove', params=words[1:], ctx=ctx)
        trigger = gif_triggers.get_trigger(name=words[1])
        if trigger is not None and len(words) >= 3 and words[2].isdigit():
            ans = gif_triggers.remove_gif_by_number(group_name=trigger.name, number=int(words[2])-1)
            if ans == -1:
                await dilogcomm.bomb_message(ctx=ctx, message='Ошибка в команде', type='error')
            else:
                await dilogcomm.bomb_message(ctx=ctx, message='Из триггера <{0}> удалена gif:\n{1}'.format(
                    trigger.name, ans))
        else:
            await dilogcomm.bomb_message(ctx=ctx, message='Ошибка в ключевом слове или номере gif', type='error')

    else:                           # ===== ВЫЗОВ GIF
        await  dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвал команду -t (вызов триггера)', params=words, ctx=ctx)
        trigger = gif_triggers.get_trigger(name=words[0])
        if trigger is not None:
            if len(ctx.message.mentions) > 0:
                text = ctx.author.mention + ' ' + trigger.discr + ' ' + ctx.message.mentions[0].mention
                url = gif_triggers.get_random_gif(words[0])
                await ctx.send(text + '\n' + url)
            elif len(words) > 1:
                if words[1].isdigit():
                    await ctx.send(gif_triggers.get_gif_by_number(group_name=words[0], number=int(words[1])-1))
            else:
                await ctx.send(gif_triggers.get_random_gif(words[0]))
        else:
            await dilogcomm.bomb_message(ctx=ctx, message='ошибка в ключевом слове или команде', type='error')


# Поиск gif (дял команды выше)
async def search_gif_mes(ctx):
    a = ctx.author.id
    async for message in ctx.channel.history(limit=10, oldest_first=False):
        a = message.author.id
        if messages_proc.is_gif(message=message):
            await message.delete()
            return message.content
    return None


# Блокировка комманд
# @bot.command()
# @commands.has_guild_permissions(administrator=True)
# async def block(ctx):
#     await ctx.message.delete()
#     global is_calculating
#     is_calculating = not is_calculating
#     await ctx.send(str(is_calculating))


# Тестовое сообщение от бота
@bot.command()
async def tm(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await simplecomm.hello(ctx)


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


# Считает статистику
@bot.command()
async def calc(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_calc, ctx, False, True, words)


async def _calc(ctx: discord.ext.commands.Context, *words):
    newstat: userstatslist.UserStatsList = await datacommm.calculate_txtchannel_stats(ctx.channel)
    answer = ''
    for curr_stat in newstat:
        answer += '{0} напечатал {1} символов\n'.format(curr_stat.name, curr_stat.symb_counter)
    await ctx.send('```{0}```'.format(answer))


# Считает всю статистику
@bot.command()
@commands.has_guild_permissions(administrator=True)
async def calc_all(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_calc_all, ctx, False, True, words)


async def _calc_all(ctx: discord.ext.commands.Context, *words):
    await ctx.send('```{0}```'.format(await datacommm.print_all_txtchannel_stats(ctx=ctx)))


@bot.command(name='print')
async def printer(ctx: discord.ext.commands.Context, *words):
    await ctx.message.delete()
    await ctx.send(str(ctx.message.content))


@bot.command(name='read')
async def reader(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    print(str(ctx.message.content))


# ======================================================================================================================
# ОБЩИЕ КОМАНДЫ
# ======================================================================================================================


# Показывает статистику указанного пользователя
@bot.command(name='stat')
async def stat(ctx: discord.ext.commands.Context, *words):
    await stats(ctx, words)


# Показывает статистику указанного пользователя
@bot.command(name='stats')
async def stats(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_stats, ctx, False, False, words)


async def _stats(ctx: discord.ext.commands.Context, *words):
    await ctx.send(embed=datacommm.user_stats_emb(ctx=ctx, DB=DB))


# Показывает статистику указанного пользователя (старый вариант)
@bot.command(name='stats_old')
async def stats2(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_stats2, ctx, False, False, words)


async def _stats2(ctx: discord.ext.commands.Context, *words):
    await ctx.send(embed=datacommm.user_stats_emb2(ctx=ctx, DB=DB))


# Исправляет имя пользователя
@bot.command(name='fixname')
async def fix_name(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_fix_name, ctx, False, False, words)


async def _fix_name(ctx: discord.ext.commands.Context, *words):
    stat: userstats.userstats = DB.select(ctx.message.author.id)
    stat.name = ctx.message.author.name + '#' + str(ctx.message.author.discriminator)
    DB.update(stat=stat)


# Выдаёт информацию о коммандах
@bot.command(name='помощь')
async def help_info(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_help_info, ctx, False, True, words)


async def _help_info(ctx: discord.ext.commands.Context, *words):
    await ctx.send('```{0}```'.format(textfile.RadAll(config.params['info'])))


# Выдаёт информацию о коммандах
@bot.command(name='last_update')
async def update_info(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_update_info, ctx, False, True, words)


async def _update_info(ctx: discord.ext.commands.Context, *words):
    await ctx.send('```{0}```'.format(textfile.RadAll(_shortcut.update)))

# Выдаёт информацию о коммандах (+комманды модераторов)
@bot.command(name='moders')
@commands.has_guild_permissions(manage_channels=True)
async def moder_info(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_moder_info, ctx, False, True, words)


async def _moder_info(ctx: discord.ext.commands.Context, *words):
    await ctx.send('```{0}\n{1}```'.format(textfile.RadAll('information/commands_help.txt'), textfile.RadAll('data\info_moders.txt')))


# ======================================================================================================================
# ФУНКЦИИ
# ======================================================================================================================


# спам линком в чате
@bot.command()
async def bomb(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_bomb, ctx, False, False, words)


async def _bomb(ctx: discord.ext.commands.Context, *words):
    ans = None
    mes, link = simplecomm.extract_links_from_params_list(ctx.message)
    mes = ' '.join(mes[1:])
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвана команда -bomb'.format(ctx.message.author.name),
                             params=['bomb', link, mes])
    if ctx.author.id in exe_list:
        await ctx.send('```команда уже выполняется```')
        return
    exe_list.append(ctx.author.id)

    if roles_proc.is_exist(rolelist=ctx.author.roles, serchrole=roles_configs.ban_functions):
        return

    if await simplecomm.bomb(ctx=ctx, text=mes) == -2:
        ans = -2
    exe_list.pop(exe_list.index(ctx.author.id))
    return ans


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


# ======================================================================================================================
# ГРУППА ИНФОРМАЦИОННЫХ КОМАНД
# ======================================================================================================================


# Общая функция группы
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


# ======================================================================================================================
# ГРУППА КОМАНД МОДЕРАЦИИ
# ======================================================================================================================


# Общая функция группы
@bot.group(nane='mod')
@commands.has_guild_permissions(manage_channels=True)
async def mod(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Останавливает выполнение комманд
@mod.command(name='stop')
async def commands_stop(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.author,
                             message='вызвана комманда stop]\n[выполение активных комманд будет прервано')
    simplecomm.stop_exe = True
    await asyncio.sleep(20)
    simplecomm.stop_exe = False


# Утсанавливает роль для мута
@mod.command(name='moot')
async def give_moot(ctx: discord.ext.commands.Context):
    await moderationcomm.give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=roles_configs.moot)


# Утсанавливает роль для войс мута
@mod.command(name='voicemoot')
async def give_voice_moot(ctx: discord.ext.commands.Context):
    await moderationcomm.\
        give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=roles_configs.vc_moot)


# Утсанавливает роль с ограниченныи функциями
@mod.command(name='banfunc')
async def give_ban_func(ctx: discord.ext.commands.Context):
    await moderationcomm.\
        give_timer_role(bot=bot, ctx=ctx, RoleList=guild.roles, rolename=roles_configs.ban_functions)


# Удаление сообщений
@mod.command(name='clearmes')
async def clearmes(ctx: discord.ext.commands.Context):
    await moderationcomm.deletemessages(bot, ctx=ctx, DB=DB)


# ======================================================================================================================
# ГРУППА КОМАНД НАСТРОЕК
# ======================================================================================================================


# Общая функция группы
@bot.group(nane='set')
@commands.has_guild_permissions(manage_channels=True)
async def set(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Показывает настройки
@set.command(name='show')
async def show_configs(ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.author, message='вызвана комманда -set show')
    await ctx.send('```general:\n{0}\nroles:\n{1}```'.format(gen_configs.print(), roles_configs.print()))


# меняет основные настройки
@set.command(name='general')
async def set_general(ctx: discord.ext.commands.Context, *words):
    if gen_configs.set_by_key(key=words[0], value=int(words[1])) == 0:
        await dilogcomm.printlog(bot=bot, author=ctx.author, message='настройка {0} изменена на {1}'.
                                 format(words[0], words[1]))
        await dilogcomm.bomb_message(ctx=ctx, message='настройка {0} изменена на {1}'.format(words[0], words[1]))
    else:
        await dilogcomm.bomb_message(ctx=ctx, message='введено неверное название праметра', type='error')


# меняет настройки ролей
@set.command(name='roles')
async def set_roles(ctx: discord.ext.commands.Context, *words):
    value = ' '.join(words[1:])
    if roles_proc.is_exist(rolelist=guild.roles, serchrole=value):
        if roles_configs.set_by_key(key=words[0], value=value) == 0:
            await dilogcomm.printlog(bot=bot, author=ctx.author, message='настройка {0} изменена на {1}'.
                                     format(words[0], words[1]))
            await dilogcomm.bomb_message(ctx=ctx, message='настройка {0} изменена на {1}'.format(words[0], words[1]))
        else:
            await dilogcomm.bomb_message(ctx=ctx, message='введено неверное название праметра', type='error')
    else:
        await dilogcomm.bomb_message(ctx=ctx, message='указанная роль не существует', type='error')


# ======================================================================================================================
# ГРУППА СИСТЕМНЫХ КОММАНД
# ======================================================================================================================


# Общая функция группы
@bot.group(nane='sys')
@commands.has_guild_permissions(manage_channels=True)
async def sys(ctx: discord.ext.commands.Context):
    await ctx.message.delete()


# Перерассчитывает статистику по сообщениям на сервере
@sys.command(name='recalc_stats')
@commands.has_guild_permissions(administrator=True)
async def sys_recalc_all(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_sys_recalc_all, ctx, False, True, words)


async def _sys_recalc_all(ctx: discord.ext.commands.Context, *words):
    global DB
    new_stats = []
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
    for curr_stat in new_stats:
        answer += '{0} напечатал {1} символов\n'.format(curr_stat.name, curr_stat.symb_counter)
    await dilogcomm.printlog(bot=bot, message=answer)


# Перерассчитывает опыт и перезаписывает имена всех пользователей
@sys.command(name='fix_stats')
async def fix_stats(ctx: discord.ext.commands.Context, *words):
    await correct_boot(_sys_recalc_all, ctx, False, True, words)


async def _fix_stats(ctx: discord.ext.commands.Context, *words):
    global DB
    curr_stats: userstats.userstats
    for member in ctx.author.guild.members:
        curr_stats = DB.select(member.id)
        if curr_stats is None:
            DB.insert(userstats.userstats(ID=member.id, Name=member.name))
        else:
            curr_stats.calculate_exp()
            curr_stats.name = member.name
            DB.update(stat=curr_stats)
    await dilogcomm.printlog(bot=bot,
                             message='статистика опыта и имена пользователей обновлены'.format(ctx.message.author.name))


# команда завершения работы
@sys.command(name='off')
async def sys_shutdown(ctx: discord.ext.commands.Context):
    global sys_boot
    await update_write_time()
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='инициировано выключение'.format(ctx.message.author.name))
    await dilogcomm.printlog(bot=bot, message='bot offline')
    sys_boot = False
    await bot.close()


async def update_data_loop():
    while sys_boot:
        print('time written')
        await update_write_time(print_log=False)
        await asyncio.sleep(gen_configs.time_update_delay)


# обновляет время последней записи
async def update_write_time(print_log: bool = True):
    params.shutdownparams['time'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
    textfile.WriteParams(params.shutdownparams, config.params['shutdown_info'], delsymb='=')
    if print_log:
        await dilogcomm.printlog(bot=bot, message='обновлено время последней записи {0} UTC+0:00'.
                                 format(params.shutdownparams['time']))


# Обращаемся к словарю settings с ключом token, для получения токена
print('boot')
bot.run(con_config.settings['token'])
