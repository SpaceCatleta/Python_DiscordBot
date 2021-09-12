import discord
from botdb.entities import GeneralSettings, Guild, User, GifGroup, Gif

bot: discord.Client


async def print_gif_group(gifGroup: GifGroup.GifGroup, gifCount: int):
    user = await bot.fetch_user(user_id=gifGroup.authorId)
    return "ключевое слово: {0}   фраза: {1}\n" \
           "автор: {2}   дата создания: {3}\n" \
           "доступ всем: {4}   кол-во gif: {5}" \
           "".format(gifGroup.name, gifGroup.phrase, user.name + '#' + user.discriminator,
                     gifGroup.createDate, gifGroup.accessLevel, gifCount)
