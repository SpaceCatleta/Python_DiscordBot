import discord
from discord.ext import commands
from config import settings
import mycommands

# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
bot = commands.Bot(command_prefix=settings['prefix'])
guild: discord.Guild
UserKeys = []
UserCounter = []


@bot.event
async def on_ready():
    global guild, UserKeys, UserCounter
    guild = bot.get_guild(settings['home_guild_id'])
    print(len(guild.members))
    for user in guild.members:
        UserKeys.append(user.id)
        UserCounter.append(0)
    print('loading finished')



@bot.event
async def on_message(mes: discord.Message):
    if mes.author.bot:
        return
    UserCounter[UserKeys.index(mes.author.id)] += len(mes.content)
    await bot.process_commands(mes)


@bot.command()
async def tm(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    await mycommands.hello(ctx)


@bot.command()
async def stats(ctx: discord.ext.commands.Context):
    await ctx.message.delete()
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    await ctx.send('```Напечатано символов: ' + str(UserCounter[UserKeys.index(user.id)]) + '```')


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
    await ctx.send('```ID сервера: ' + str(ctx.author.guild.id) + '```')


# команда завершения работы
@bot.command()
async def off(ctx: discord.ext.commands.Context):
    await ctx.send('```[bot offline]```')
    exit()


# спам линком в чате
@bot.command()
async def bomb(ctx: discord.ext.commands.Context):
    if len(ctx.message.mentions) > 0:
        link = ctx.message.mentions[0]
        for i in range(0, 10):
            await ctx.send(link.mention)


# Обращаемся к словарю settings с ключом token, для получения токена
print('boot bot...')
bot.run(settings['token'])
