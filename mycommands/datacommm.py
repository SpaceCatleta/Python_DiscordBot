import discord
import time
from generallib import mainlib, structs
from mycommands import dilogcomm


# Возващает статистику пользователя
def user_stats(ctx: discord.ext.commands.Context, StatsList):
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    stat: structs.userstats = structs.searchid(StatsList, user.id)
    if stat is not None:
        stat.exp = round(stat.exp, 1)
        answerstr = '''{0}:\nОпыт: {1}\nОтправлено сообщений: {2}\nНапечатано символов: {3}\nВремя в голосовых чатах:\
 {4}'''.format(user.display_name, mainlib.print_number(stat.exp, 1), stat.mes_counter, stat.symb_counter,
               time.strftime("%H:%M:%S", time.gmtime(stat.vc_counter)).replace(' ', ''))
        return answerstr
    else:
        return str(user.display_name + ' - Данные не найдены')


# Возващает статистику пользователя для Embed
def user_stats_emb(ctx: discord.ext.commands.Context, StatsList):

    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    stat: structs.userstats = structs.searchid(StatsList, user.id)
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


# Обновляет статистику пользователя по отправленному им сообщщению
def stats_update(mes: discord.Message, StatsList):
    if mes.author.bot:
        return
    stat: structs.userstats = structs.searchid(StatsList, mes.author.id)
    if stat is not None:
        symbprint = mainlib.mylen(mes.content)
        stat.symb_counter += symbprint
        stat.mes_counter += 1
        stat.exp += symbprint/10
    else:
        newstat = structs.userstats(ID=mes.author.id, )
        symbprint = mainlib.mylen(mes.content)
        newstat.symb_counter += symbprint
        newstat.mes_counter += 1
        newstat.exp += symbprint / 10
        StatsList.append(newstat)


async def voice_stats_update(bot, Stats_List, member: discord.Member,
                             before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None:
        user = structs.searchid(list=Stats_List, ID=member.id)
        user.connect_time = time.time()
    if after.channel is None:
        user = structs.searchid(list=Stats_List, ID=member.id)
        user.name = member.name
        chat_time = time.time() - user.connect_time
        if chat_time > 10000000:
            await dilogcomm.printlog(bot=bot, message='{0} - ошибка вычисления в гс чате [{1}]'.
                                     format(user.name, chat_time))
        else:
            user.vc_counter += chat_time
            await dilogcomm.printlog(bot=bot, message='{0} пробыл в гс {1}сек.'.format(user.name, chat_time))
