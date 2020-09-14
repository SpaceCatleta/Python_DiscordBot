import discord
import structs
import TextFile as TFile
import config
import GeneralLib
from discord.ext import commands
from con_config import settings
from mycommands import simplecomm, dilogcomm, moderationcomm, systemcomm, datacommm


# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
bot = commands.Bot(command_prefix=settings['prefix'])
guild: discord.Guild
UserStats = []


@bot.event
async def on_ready():
    global guild, UserStats
    guild = bot.get_guild(settings['home_guild_id'])
    readlist = TFile.ReadSymbolsStat(config.params['SymbolsStatisticsFile'])
    if len(readlist) == 0:
        for user in guild.members:
            UserStats.append(structs.userstats(user.id, 0))
    else:
        UserStats = readlist
    TCh: discord.channel = bot.get_channel(settings['home_guild_logs_channel'])
    await TCh.send('```[bot online]```')


@bot.event
async def on_message(mes: discord.Message):
    if mes.author.bot:
        return
    global UserStats
    stat: structs.userstats = structs.searchid(UserStats, mes.author.id)
    if stat is not None:
        stat.counter += GeneralLib.mylen(mes.content)
    else:
        UserStats.append(structs.userstats(ID=mes.author.id, Counter=GeneralLib.mylen(mes.content)))
    await bot.process_commands(mes)


@bot.command()
async def info(ctx: discord.ext.commands.Context, **kwargs):
    await ctx.message.delete()
    await ctx.send('```' + TFile.RadAll(config.params['info']) + '```')


@bot.command()
async def tm(ctx: discord.ext.commands.Context, **kwargs):
    await ctx.message.delete()
    await simplecomm.hello(ctx)


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
    stat: structs.userstats = structs.searchid(UserStats, user.id)
    if stat is not None:
        await ctx.send('```' + user.display_name + ' - напечатано символов: ' + str(stat.counter) + '```')


@bot.command()
async def statsdown(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    per: discord.permissions = ctx.message.author.permissions_in(ctx.channel)
    if not per.manage_channels:
        return
    await datacommm.ChangeSymbStats(bot=bot, ctx=ctx, StatsList=UserStats)


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
    TCh: discord.channel = bot.get_channel(settings['home_guild_logs_channel'])
    await TCh.send('```[bot offline]```')
    await bot.close()


# спам линком в чате
@bot.command()
async def bomb(ctx: discord.ext.commands.Context):
    per: discord.permissions = ctx.message.author.permissions_in(ctx.channel)
    if not per.manage_channels:
        print('vvv')
    await simplecomm.bomb(ctx)


@bot.command()
async def syschannel(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    TCh: discord.TextChannel = ctx.guild.system_channel
    if TCh is None:
        await ctx.send('```Системный канал не установлен```')
    else:
        await TCh.send('```This is system channel```')


@bot.command()
async def channelid(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await ctx.send('```Channel id: ' + str(ctx.channel.id) + '```')


@bot.command()
async def updateschannel(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    TCh: discord.TextChannel = ctx.guild.public_updates_channel
    if TCh is None:
        await ctx.send('```Канал для публичных обновлений не установлен```')
    else:
        await TCh.send('```This is public updates channel```')


@bot.command(pass_context = True)
async def clearmes(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    per: discord.permissions = ctx.message.author.permissions_in(ctx.channel)
    if not per.manage_channels:
        return
    await moderationcomm.deletemessages(bot, ctx=ctx, stats=UserStats)


# Обращаемся к словарю settings с ключом token, для получения токена
print('boot bot...')
bot.run(settings['token'])
