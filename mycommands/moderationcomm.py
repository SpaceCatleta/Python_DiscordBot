import discord
import structs
import GeneralLib
from mycommands import dilogcomm


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
    await dilogcomm.printlog(bot, ctx.author, 'С канала ' + ctx.channel.name + ' удалено ' + str(n) + ' сообщений' + addlog)


# Обнуляет символы в статистике, полученные за указанные сообщения
async def DeleteExp(MesList, StatsList):
    deflog: str = ""
    authorsdata = []

    for mes in MesList:
        if mes.author.bot:
            continue
        counter = GeneralLib.mylen(mes.content)
        ID = mes.author.id
        user = structs.searchid(authorsdata, ID)
        if user is None:
            user = structs.userdata(Name=mes.author.name, ID=mes.author.id, Counter=0)
            authorsdata.append(user)
        user.counter += counter

    for author in authorsdata:
        userstat: structs.userstats = structs.searchid(StatsList, author.id)
        userstat.counter -= author.counter
        deflog += '\n  > ' + author.name + ' статистика символов понижена на ' + str(author.counter)
    return deflog
