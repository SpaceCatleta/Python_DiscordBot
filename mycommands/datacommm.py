import discord
import time
from generallib import mainlib
from structs import userstats
from mycommands import dilogcomm
from data import sqlitedb


# Возващает статистику пользователя
def get_user_stats(ctx, DB: sqlitedb.BotDataBase):
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    stat: userstats.userstats = DB.select(user.id)
    if stat is not None:
        stat.exp = round(stat.exp, 1)
        answerstr = '''{0}:\nОпыт: {1}\nОтправлено сообщений: {2}\nНапечатано символов: {3}\nВремя в голосовых чатах:\
 {4}'''.format(user.display_name, mainlib.print_number(stat.exp, 1), stat.mes_counter, stat.symb_counter,
               time.strftime("%H:%M:%S", time.gmtime(stat.vc_counter)).replace(' ', ''))
        return answerstr
    else:
        return str(user.display_name + ' - Данные не найдены')


# Возващает статистику пользователя для Embed
def user_stats_emb(ctx, DB: sqlitedb.BotDataBase):

    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    stat: userstats.userstats = DB.select(user.id)
    answer = ['Статистика {0}:'.format(user.display_name)]
    if stat is not None:
        stat.exp = round(stat.exp, 1)
        answer_str = 'Опыт: {0}\nОтправлено сообщений: {1}\nНапечатано символов: {2}\nВремя в голосовых чатах:\
 {3}'.format(mainlib.print_number(stat.exp, 1), stat.mes_counter, stat.symb_counter,
             time.strftime("%H:%M:%S", time.gmtime(stat.vc_counter)).replace(' ', ''))
        answer.append(answer_str)
        return answer
    else:
        return str(user.display_name + ' - Данные не найдены')


# Расчитывает статистику на всех текстовых каналах с указанного времени
async def calc_alltxtchannels_stats_after_time(guild: discord.Guild, time, DB: sqlitedb.BotDataBase):
    StatList = []
    for channel in guild.channels:
        if issubclass(type(channel), discord.TextChannel):
            StatList = merge_stats(StatList, await calc_stats_after_time(channel=channel, time=time))
    deflog = 'Был произведён поиск сообщений после последней записи статистики'
    for user in StatList:
        deflog += '\n > {0} > обнаружено: {1} сообщений, {2} символов;\
 начислено {3} опыта'.format(user.name, user.mes_counter, user.symb_counter,  mainlib.print_number(user.exp, 1))
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


# Обновляет статистику пользователя по отправленному им сообщщению
def stats_update_list(mes: discord.Message, StatsList: list):
    if mes.author.bot:
        return
    stat: userstats.userstats = userstats.searchid(ID=mes.author.id, List=StatsList)
    if stat is not None:
        symbprint = mainlib.mylen(mes.content)
        stat.symb_counter += symbprint
        stat.mes_counter += 1
        stat.exp += symbprint/10
    else:
        newstat = userstats.userstats(ID=mes.author.id)
        symbprint = mainlib.mylen(mes.content)
        newstat.symb_counter += symbprint
        newstat.mes_counter += 1
        newstat.exp += symbprint / 10
        newstat.name = mes.author.name + str(mes.author.discriminator)
        StatsList.append(newstat)


# Обновляет статистику пользователя по отправленному им сообщщению
def stats_update(mes: discord.Message, DB: sqlitedb.BotDataBase):
    if mes.author.bot:
        return
    stat: userstats.userstats = DB.select(mes.author.id)
    if stat is not None:
        symbprint = mainlib.mylen(mes.content)
        stat.symb_counter += symbprint
        stat.mes_counter += 1
        stat.exp += symbprint/10
        DB.update(stat=stat)
    else:
        newstat = userstats.userstats(ID=mes.author.id)
        symbprint = mainlib.mylen(mes.content)
        newstat.symb_counter += symbprint
        newstat.mes_counter += 1
        newstat.exp += symbprint / 10
        newstat.name = mes.author.name + str(mes.author.discriminator)
        DB.insert(stat=newstat)


async def voice_stats_update(bot, DB: sqlitedb.BotDataBase, member: discord.Member,
                             before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None:
        user = DB.select(member.id)
        user.connect_time = time.time()
    if after.channel is None:
        user = DB.select(member.id)
        user.name = member.name
        chat_time = time.time() - user.connect_time
        if chat_time > 10000000:
            await dilogcomm.printlog(bot=bot, message='{0} - ошибка вычисления в гс чате [{1}]'.
                                     format(user.name, chat_time))
        else:
            user.vc_counter += chat_time
            DB.update(stat=user)
            await dilogcomm.printlog(bot=bot, message='{0} пробыл в гс {1}сек.'.format(user.name, chat_time))


async def calculate_txtchannel_stats(channel):
    newstat = []
    async for mes in channel.history(limit=10000, oldest_first=None):
        stats_update(mes, newstat)
    return newstat


def merge_stats(stats1, stats2):
    for stat in stats2:
        stat1 = userstats.searchid(stats1, stat.id)
        if stat1 is not None:
            stat1.add(stat)
        else:
            stats1.append(stat)
    return stats1