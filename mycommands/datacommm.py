import discord
from generallib import structs
from mycommands import dilogcomm


# Возващает статистику пользователя
async def userstats(ctx: discord.ext.commands.Context, StatsList):
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    stat: structs.userstats = structs.searchid(StatsList, user.id)
    if stat is not None:
        return str(user.display_name + ' - напечатано символов: ' + str(stat.counter))
    else:
        return str(user.display_name + ' - Данные не найдены')


async def ChangeSymbStats(bot, ctx: discord.ext.commands.Context, StatsList):
    STR: str = ctx.message.content
    LIST = STR.split(' ')
    if len(LIST) > 2:
        print(str(LIST[2]))
        n: int = int(LIST[2])
    else:
        n = 100
    if len(ctx.message.mentions) == 0:
        return
    user: discord.abc.User = ctx.message.mentions[0]
    stat: structs.userstats = structs.searchid(StatsList, user.id)
    stat.counter -= n
    await dilogcomm.printlog(bot, ctx.author, 'Статистика ' + user.name + ' понижена на ' + str(n) + ' символов')