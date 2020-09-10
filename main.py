import discord
from discord.ext import commands
from config import settings
import mycommands

# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
bot = commands.Bot(command_prefix=settings['prefix'])
UserKeys = []
UserCounter = []


# Не передаём аргумент pass_context, так как он был нужен в старых версиях.
# ctx <Context> - контекст комманды
@bot.command()
async def tm(ctx: discord.ext.commands.Context):  # Создаём функцию и передаём аргумент ctx.
    await mycommands.hello(ctx)


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


# команда завершения работы
@bot.command()
async def off(ctx: discord.ext.commands.Context):
    await ctx.send('[bot was turned off]')
    exit()


# спам линком в чате
@bot.command()
async def bomb(ctx: discord.ext.commands.Context):
    if len(ctx.message.mentions) > 0:
        link = ctx.message.mentions[0]
        for i in range(0, 10):
            await ctx.send(link.mention)


# событие при поступлении сообщения в чат
# 'mes' <Message> - отправленное сообщение
@bot.event
async def on_message(mes: discord.Message):
    if mes.author.bot:
        return
    # await mlen: int = len(mes.content)
    # await mes.channel.send(mes.author.mention)
    await bot.process_commands(mes)


# Обращаемся к словарю settings с ключом token, для получения токена
print('boot bot...')
bot.run(settings['token'])
