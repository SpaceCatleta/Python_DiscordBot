import discord
import asyncio

from processing import roles_proc, messages_proc
from structs import userstats
from mycommands import dilogcomm, simplecomm
from data import sqlitedb


# Удаляет переданное в сообщении кол-во сообщений
async def deletemessages(bot, ctx: discord.ext.commands.Context, DB: sqlitedb.BotDataBase):
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
            addlog = await DeleteExp(MesList=meslist, DB=DB)
    await TCH.delete_messages(meslist)
    await dilogcomm.printlog(bot=bot, author=ctx.author,message='Вызвана команада удаления сообщений',
        params=simplecomm.create_params_list_removing_links_to_str(ctx.message))
    await dilogcomm.printlog(bot=bot, message='С канала "{0}"\
 удалено {1} сообщений {2}'.format(ctx.channel.name, str(n), addlog))


# Обнуляет символы в статистике, полученные за указанные сообщения
async def DeleteExp(MesList, DB: sqlitedb.BotDataBase):
    deflog: str = ""
    authorsdata = []

    # Вычесление удаляемого опыта
    for mes in MesList:
        if mes.author.bot:
            continue
        user = userstats.searchid(authorsdata, mes.author.id)
        # Если пользователь попадается впервые, создаётся новый объект
        if user is None:
            user = userstats.userstats(ID=mes.author.id)
            user.name = mes.author.name
            authorsdata.append(user)
        # Вычисление и запись поинжаемых статистик
        symb_counter = messages_proc.text_len(mes.content)
        user.symb_counter -= symb_counter
        user.exp -= symb_counter / 10
        user.mes_counter -= 1

    # Понижение статистик и логирование
    for author in authorsdata:
        DB.update_with_addition(stat=author)
        deflog += '\n > {0} > удалено: {1} сообщений, {2} символов,\
 {3} опыта'.format(author.name, author.mes_counter, author.symb_counter,  author.exp)
    return deflog


# Даёт роль на указанное кол-во секунд
async def give_timer_role(bot, ctx: discord.ext.commands.Context, RoleList: list, rolename: str):
    if len(ctx.message.mentions) == 0:
        return -1
    mootrole = roles_proc.find_role(rolelist=RoleList, serchrole=rolename)
    user: discord.Member = ctx.message.mentions[0]
    arglist = ctx.message.content.split(' ')
    n = 600 if len(arglist) < 3 else int(arglist[2])
    await user.add_roles(mootrole)

    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='пользователю {0} выдана роль "{1}" на {2} сек.'.format(user.name, rolename, n))
    await ctx.send('```пользователю {0} выдана роль "{1}" на {2} сек.```'.format(user.name, rolename, n))

    await asyncio.sleep(n)
    await user.remove_roles(mootrole)
