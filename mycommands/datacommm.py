import discord
import time
from generallib import mainlib
from structs import userstats, userstatslist
from mycommands import dilogcomm
from data import sqlitedb


# Возващает статистику пользователя
def get_user_stats(ctx, DB: sqlitedb.BotDataBase):
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    stat: userstats.userstats = DB.select(user.id)
    if stat is not None:
        stat.exp = round(stat.exp, 1)
        answerstr = '''{0}:\nОпыт: {1}\nОтправлено сообщений: {2}\nНапечатано символов: {3}\nВремя в голосовых чатах:\
 {4}'''.format(user.display_name, round(stat.exp, 1), stat.mes_counter, stat.symb_counter,
               time.strftime("%H:%M:%S", time.gmtime(stat.vc_counter)).replace(' ', ''))
        return answerstr
    else:
        return str(user.display_name + ' - Данные не найдены')


# Возващает статистику пользователя для Embed
def user_stats_emb2(ctx, DB: sqlitedb.BotDataBase):

    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    stat: userstats.userstats = DB.select(user.id)
    if stat is None:
        return discord.Embed(description=user.display_name + ' - Данные не найдены')
    title = 'Статистика {0}:'.format(user.display_name)
    discr = 'Опыт: {0}\nОтправлено сообщений: {1}\nНапечатано символов: {2}\nВремя в голосовых чатах:\
 {3}'.format(round(stat.exp, 1), stat.mes_counter, stat.symb_counter,
             time.strftime("%H:%M:%S", time.gmtime(stat.vc_counter)).replace(' ', ''))
    emb: discord.Embed = discord.Embed(color=discord.colour.Color.dark_magenta(),
                                       title=title, description=discr)
    return emb


# Возващает статистику пользователя для Embed
def user_stats_emb(ctx, DB: sqlitedb.BotDataBase) -> discord.Embed:
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    stat: userstats.userstats = DB.select(user.id)
    if stat is None:
        return discord.Embed(description=user.display_name + ' - Данные не найдены')
    emb: discord.Embed = discord.Embed(color=discord.colour.Color.dark_magenta(),
                                       title='Пользователь {0}:'.format(user.display_name))
    emb.set_thumbnail(url=user.avatar_url)
    emb.add_field(name='Уровень:', value=stat.lvl)
    emb.add_field(name='Опыт:', value=str(round(stat.exp, 1)) + '/99999')
    emb.add_field(name='Статистика:', value='Отправлено сообщений: {0}\nНапечатано символов: {1}\
    \nВремя в голосовых чатах:{2}'.format(stat.mes_counter, stat.symb_counter,
        time.strftime("%H:%M:%S", time.gmtime(stat.vc_counter)).replace(' ', '')), inline=False)
    return emb


# Расчитывает статистику на всех текстовых каналах с указанного времени
async def calc_alltxtchannels_stats_after_time(guild: discord.Guild, time, DB: sqlitedb.BotDataBase):
    StatList = []
    for channel in guild.channels:
        if issubclass(type(channel), discord.TextChannel):
            StatList = merge_stats(StatList, await calc_stats_after_time(channel=channel, time=time))
    deflog = 'Был произведён поиск сообщений после последней записи статистики'
    for user in StatList:
        deflog += '\n > {0} > обнаружено: {1} сообщений, {2} символов;\
 начислено {3} опыта'.format(user.name, user.mes_counter, user.symb_counter,  round(user.exp, 1))
    for stat in StatList:
        if DB.select(stat.id) is None:
            DB.insert(stat)
        else:
            DB.update_with_addition(stat=stat)
    return deflog


# Расчитывает статистику на текстовом канале с указанного времени
async def calc_stats_after_time(channel: discord.TextChannel, time):
    StatList = []
    async for message in channel.history(limit=10000, oldest_first=False, after=time):
        stats_update_list(message, StatList)
    return StatList


# Обновляет статистику пользователя по отправленному им сообщению (для списков)
def stats_update_list(mes: discord.Message, StatsList: list):
    if mes.author.bot:
        return
    stat: userstats.userstats = userstats.searchid(ID=mes.author.id, List=StatsList)
    if stat is not None:
        stat.add_messages_stat(symbols=mainlib.mylen(mes.content), messages=1)
    else:
        newstat = userstats.userstats(ID=mes.author.id)
        newstat.add_messages_stat(symbols=mainlib.mylen(mes.content), messages=1)
        newstat.name = mes.author.name + str(mes.author.discriminator)
        StatsList.append(newstat)


# Обновляет статистику пользователя по отправленному им сообщщению (для спец. класса-списка)
def stats_update_userstatlist(mes: discord.Message, StatsList: userstatslist.UserStatsList):
    if mes.author.bot:
        return
    stat: userstats.userstats = StatsList.search_id(ID=mes.author.id)
    if stat is not None:
        stat.add_messages_stat(symbols=mainlib.mylen(mes.content), messages=1)
    else:
        newstat = userstats.userstats(ID=mes.author.id)
        newstat.add_messages_stat(symbols=mainlib.mylen(mes.content), messages=1)
        newstat.name = mes.author.name + str(mes.author.discriminator)
        StatsList.push(newstat)


# Обновляет статистику пользователя по отправленному им сообщщению (для базы данных)
def stats_update(mes: discord.Message, DB: sqlitedb.BotDataBase):
    if mes.author.bot:
        return
    stat: userstats.userstats = DB.select(mes.author.id)
    if stat is not None:
        stat.add_messages_stat(symbols=mainlib.mylen(mes.content), messages=1)
        DB.update(stat=stat)
    else:
        newstat = userstats.userstats(ID=mes.author.id)
        newstat.add_messages_stat(symbols=mainlib.mylen(mes.content), messages=1)
        newstat.name = mes.author.name + str(mes.author.discriminator)
        DB.insert(stat=newstat)


# обновляет статистику из гс
async def voice_stats_update(bot, DB: sqlitedb.BotDataBase, member: discord.Member,
    Processing: userstatslist.UserStatsList, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None:
        user = userstats.userstats(ID=member.id)
        user.connect_time = time.time()
        Processing.push(user)
    if after.channel is None:
        user = Processing.pop_by_id(ID=member.id)
        vc_time_counter = time.time() - user.connect_time
        user.vc_counter = time.time() - user.connect_time
        if vc_time_counter > 10000000:
            await dilogcomm.printlog(bot=bot, message='{0} - ошибка вычисления времени в гс чате [{1}]'.
                                     format(member.name, vc_time_counter))
        else:
            DB.update_with_addition(stat=user)
            await dilogcomm.printlog(bot=bot, message='{0} пробыл в гс {1}сек.'.format(member.name, vc_time_counter))


# вычисляет статистику одного текстового канала
async def calculate_txtchannel_stats(channel):
    newstat = userstatslist.UserStatsList()
    async for mes in channel.history(limit=10000, oldest_first=None):
        stats_update_userstatlist(mes=mes, StatsList=newstat)
    return newstat


# вычисляет и статистику со всех текстовых каналов
async def calculate_all_txtchannel_stats(ctx) -> userstatslist.UserStatsList:
    g = ctx.author.guild
    new_stats: userstatslist.UserStatsList = userstatslist.UserStatsList()
    counter: int = 0
    for channel in g.channels:
        if issubclass(type(channel), discord.TextChannel):
            counter += 1
            new_stats.merge_with(await calculate_txtchannel_stats(channel))
    return new_stats


# вычисляет и печатает статистику со всех текстовых каналов
async def print_all_txtchannel_stats(ctx):
    stats = await calculate_all_txtchannel_stats(ctx=ctx)
    answer = 'статистика из всех каналов:\n'
    for stat in stats:
        answer += '{0} напечатал {1} символов\n'.format(stat.name, stat.symb_counter)
    return answer


# сливает два списка со статистикой в один
def merge_stats(stats1, stats2):
    for stat in stats2:
        stat1 = userstats.searchid(stats1, stat.id)
        if stat1 is not None:
            stat1.add(stat)
        else:
            stats1.append(stat)
    return stats1