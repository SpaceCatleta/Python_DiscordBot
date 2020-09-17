import discord
import time
from generallib import mainlib, structs
from mycommands import dilogcomm


# Возващает статистику пользователя
def userstats(ctx: discord.ext.commands.Context, StatsList):
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    stat: structs.userstats = structs.searchid(StatsList, user.id)
    if stat is not None:
        answerstr = '''{0}:\nОпыт: {1}\nОтправлено сообщений: {2}\nНапечатано символов: {3}\nВремя в голосовых чатах:
        {4}'''.format(user.display_name, str(stat.exp), str(stat.mes_counter), str(stat.symb_counter),
                      time.strftime("%H:%M:%S", time.gmtime(stat.vc_counter)).replace(' ', ''))
        return answerstr
    else:
        return str(user.display_name + ' - Данные не найдены')


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
        UserStats.append(newstat)