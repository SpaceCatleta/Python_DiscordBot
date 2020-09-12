import discord
import structs
import TextFile as TFile
import config
import sys
from discord.ext import commands
from con_config import settings
import mycommands

# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
bot = commands.Bot(command_prefix=settings['prefix'])
guild: discord.Guild
UserStats = []


@bot.event
async def on_ready():
    global guild, UserStats
    guild = bot.get_guild(settings['home_guild_id'])
    print(len(guild.members))
    readlist = TFile.ReadSymbolsStat(config.params['SymbolsStatisticsFile'])
    if len(readlist) == 0:
        for user in guild.members:
            UserStats.append(structs.userstats(user.id, 0))
    else:
        UserStats = readlist

    print('arrlen-' + str(len(readlist)))
    print('loading finished')



@bot.event
async def on_message(mes: discord.Message):
    if mes.author.bot:
        return
    stat: structs.userstats = structs.searchid(UserStats, mes.author.id)
    if stat is not None:
        stat.counter += len(mes.content)
    await bot.process_commands(mes)


@bot.command()
async def tm(ctx: discord.ext.commands.Context, **kwargs):
    await ctx.message.delete()
    await mycommands.hello(ctx)


@bot.command()
async def write(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    TFile.WriteSymbolsStat(config.params['SymbolsStatisticsFile'], UserStats)
    await ctx.send('```file writed```')


@bot.command()
async def stats(ctx: discord.ext.commands.Context):
    global UserStats
    await ctx.message.delete()
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    print(user.name)
    stat: structs.userstats = structs.searchid(UserStats, user.id)
    if stat is not None:
        await ctx.send('```' + user.display_name + ' - напечатано символов: ' + str(stat.counter) + '```')


@bot.command()
async def ourguild(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    global guild
    answer = 'Название сервера: ' + guild.name + '\n'
    answer += 'Количество участников: ' + str(guild.member_count) + '\nучастники:\n'
    for user in guild.members:
        answer += user.name + ' [' + str(user.nick) + ']\n'
    await ctx.send('```' + answer + '```')


@bot.command()
async def clientdata(ctx: discord.ext.commands.Context):
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    await ctx.message.delete()
    answer = 'Основной ник: ' + user.name + '#' + user.discriminator + '\n'
    answer += 'Ник на сервере: ' + user.display_name + '\n'
    answer += 'ID: ' + str(user.id) + '\n'
    answer += 'Бот: ' + ('да' if user.bot else 'нет') + '\n'
    answer += 'Вступил: ' + str(user.joined_at) + '\n'
    await ctx.send('```' + answer + '```')


@bot.command()
async def serverid(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await ctx.send('```ID сервера: ' + str(ctx.author.guild.id) + '```')


# команда завершения работы
@bot.command()
async def off(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    TFile.WriteSymbolsStat(config.params['SymbolsStatisticsFile'], UserStats)
    await ctx.send('```[bot offline]```')
    sys.exit()


# спам линком в чате
@bot.command()
async def bomb(ctx: discord.ext.commands.Context):
    mes = ctx.message
    await ctx.message.delete()
    if len(mes.mentions) > 0:
        link = mes.mentions[0]
    elif len(mes.role_mentions) > 0:
        link = mes.role_mentions[0]
    else:
        return
    for i in range(0, 10):
        await ctx.send(link.mention)


# Обращаемся к словарю settings с ключом token, для получения токена
print('boot bot...')
bot.run(settings['token'])
