import discord


# спам линком в чате
async def bomb(ctx: discord.ext.commands.Context):
    mes = ctx.message
    if len(mes.mentions) > 0:
        link = mes.mentions[0]
    elif len(mes.role_mentions) > 0:
        link = mes.role_mentions[0]
    else:
        return
    for i in range(0, 10):
        await ctx.send(link.mention)


# Тестовое приветствие
async def hello(ctx):
    await ctx.send('1001 101 11 100 1 0')

