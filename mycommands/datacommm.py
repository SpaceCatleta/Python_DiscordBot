import discord
import structs
from mycommands import dilogcomm


async def ChangeSymbStats(bot, ctx: discord.ext.commands.Context, StatsList):
    STR: str = ctx.message.content
    LIST = STR.split(' ')
    if len(LIST) > 2:
        print(str(LIST[1]))
        n: int = int(LIST[1])
    else:
        n = 100
    if len(ctx.message.mentions) == 0:
        return
    user: discord.abc.User = ctx.message.mentions[0]
    stat: structs.userstats = structs.searchid(StatsList, user.id)
    stat.counter -= n
    await dilogcomm.printlog(bot, ctx.author, 'Статистика ' + user.name + ' понижена на ' + str(n) + ' символов')