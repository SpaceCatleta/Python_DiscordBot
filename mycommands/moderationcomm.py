import time
import discord
import asyncio
from generallib import mainlib, structs
from mycommands import dilogcomm
from usersettings import params


# Удаляет переданное в сообщении кол-во сообщений
async def deletemessages(bot, ctx: discord.ext.commands.Context, stats):
    STR: str = ctx.message.content
    LIST = STR.split(' ')
    if len(LIST) > 2:
        n: int = int(LIST[2])
    else:
        n = 10
    n = n if n <= 100 else 100

    TCH: discord.TextChannel = ctx.channel
    meslist = []
    if len(ctx.message.mentions) == 0:
        async for message in TCH.history(limit=n, oldest_first=False):
            meslist.append(message)
    else:
        mention: discord.abc.User = ctx.message.mentions[0]
        counter: int = n
        async for message in TCH.history(limit=500, oldest_first=False):
            if message.author.id == mention.id:
                meslist.append(message)
                counter -= 1
                if counter == 0:
                    break

    addlog: str = ''
    if len(LIST) > 3:
        if LIST[3] == '-exp':
            addlog = await DeleteExp(MesList=meslist, StatsList=stats)
    await TCH.delete_messages(meslist)
    await dilogcomm.printlog(bot=bot, author=ctx.author, message='С канала "{0}"\
 удалено {1} сообщений {2}'.format(ctx.channel.name, str(n), addlog))


# Обнуляет символы в статистике, полученные за указанные сообщения
async def DeleteExp(MesList, StatsList):
    deflog: str = ""
    authorsdata = []

    # Вычесление удаляемого опыта
    for mes in MesList:
        if mes.author.bot:
            continue
        user = structs.searchid(authorsdata, mes.author.id)
        # Если пользователь попадается впервые, создаётся новый объект
        if user is None:
            user = structs.userstats(ID=mes.author.id)
            user.name = mes.author.name
            authorsdata.append(user)
        # Вычисление и запись поинжаемых статистик
        symb_counter = mainlib.mylen(mes.content)
        user.symb_counter += symb_counter
        user.exp += symb_counter / 10
        user.mes_counter += 1

    # Понижение статистик и логирование
    for author in authorsdata:
        userstat: structs.userstats = structs.searchid(StatsList, author.id)
        userstat.exp -= author.exp
        userstat.symb_counter -= author.symb_counter
        userstat.mes_counter -= author.mes_counter
        deflog += '\n > {0} > удалено: {1} сообщений, {2} символов,\
 {3} опыта'.format(author.name, author.mes_counter, author.symb_counter,  author.exp)
    return deflog


# Даёт роль на указанное кол-во секунд
async def give_timer_role(bot, ctx: discord.ext.commands.Context, RoleList: list, rolename: str):
    if len(ctx.message.mentions) == 0:
        return -1
    mootrole = mainlib.Findrole(rolelist=RoleList, serchrole=rolename)
    user: discord.Member = ctx.message.mentions[0]
    arglist = ctx.message.content.split(' ')
    n = 600 if len(arglist) < 3 else int(arglist[2])
    await user.add_roles(mootrole)

    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='пользователю {0} выдана роль "{1}" на {2} сек.'.format(user.name, rolename, n))
    await ctx.send('```пользователю {0} выдана роль "{1}" на {2} сек.```'.format(user.name, rolename, n))

    await asyncio.sleep(n)
    await user.remove_roles(mootrole)
