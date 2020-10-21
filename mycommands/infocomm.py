import discord
from mycommands import dilogcomm


# Выдаёт информацию о пользователе
def get_member_information(ctx: discord.ext.commands.Context):
    user: discord.abc.User = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author
    return 'Основной ник: {0}#{1}\nНик на сервере: {2}\nID: {3}\nБот: {4}\nВступил: {5}'.\
        format(user.name, user.discriminator, user.display_name, user.id, 'да' if user.bot else 'нет', user.joined_at)


# информация о сервере
def get_guild_information(ctx: discord.ext.commands.Context):
    return 'Название сервера: {0}\nID сервера: {1}\nКоличество участников: {2}'.format(ctx.author.guild.name, ctx.author.guild.id, ctx.author.guild.member_count)


# Информация о кол-ве сообщений в канале
async def count_channel_messages(bot, ctx: discord.ext.commands.Context):
    await dilogcomm.printlog(bot=bot, author=ctx.message.author,
                             message='вызвал коанду -count'.format(ctx.message.author.name))
    counter: int = 0
    async for mes in ctx.channel.history(limit=10000, oldest_first=None):
        counter += 1
    return '''в канале "{0}" {1} сообщений'''.format(ctx.channel.name, counter)

