import discord
import _dialog
from botdb.entities.User import User as DBUser
from botdb.services import UserService


# Рассчёт количества "чистых" символов в тексте сообщения
def text_len(stroke: str):
    counter: int = 0
    isCount: bool = True
    for sym in stroke:
        if sym == '<':
            isCount = False
        elif sym == '>':
            isCount = True
            continue
        if isCount:
            counter += 1
    return counter


# Извлекает из сообщения упоминание роли
def get_role(ctx, bufferParts: int = 1):
    if len(ctx.message.role_mentions) > 0:
        return ctx.message.role_mentions[0]
    else:
        argList = ctx.message.content.split(' ')
        roleName = ' '.join(argList[bufferParts:])
        if len(argList) > bufferParts:
            answer = discord.utils.get(iterable=ctx.guild.roles, name=roleName)
            if answer is None:
                raise ValueError(f'{roleName} - название роли указано неверно')
            return answer
    return None


# Извлекает из сообщения упоминание пользователя
def get_user_link(ctx):
    if len(ctx.message.mentions) > 0:
        return ctx.message.mentions[0]
    else:
        raise ValueError('Не указан пользователь')


# Извлекает из сообщения упоминание пользователя
def get_user_link_no_exception(ctx):
    if len(ctx.message.mentions) > 0:
        return ctx.message.mentions[0]
    else:
        return None


# конвертирует строку в время в секундах
def get_time(text: str):
    text = text.lower()
    try:
        if text[-1] == 'ч' or text[-1] == 'h':
            return int(text[:-1]) * 3600
        elif text[-1] == 'м' or text[-1] == 'm':
            return int(text[:-1]) * 60
        elif text[-1] == 'с' or text[-1] == 's':
            return int(text)
        else:
            return int(text)
    except ValueError:
        raise ValueError('время введено неверно')


# Извлекает из сообщения название
def get_text_chat_link(ctx):
    print('======')
    for ch in ctx.message.channel_mentions:
        print(ch)
    print('======')
    if len(ctx.message.channel_mentions) > 0:
        return ctx.message.channel_mentions[0]
    else:
        raise ValueError('Не указан канал')


# Удаляет переданное в сообщении кол-во сообщений
async def delete_messages(bot, ctx, n, discordUser=None, isDeleteExp=False):
    n = n if n <= 100 else 100
    TCH: discord.TextChannel = ctx.channel
    messagesList = []

    # Сбор сообщений на удаление
    if discordUser is None:
        async for message in TCH.history(limit=n, oldest_first=False):
            messagesList.append(message)
    else:
        counter: int = n
        async for message in TCH.history(limit=1000, oldest_first=False):
            if message.author.id == discordUser.id:
                messagesList.append(message)
                counter -= 1
                if counter == 0:
                    break

    # Вызов удаления опыта, если требуется
    expLog: str = ''
    if isDeleteExp:
        expLog = await delete_exp(MesList=messagesList)

    await TCH.delete_messages(messagesList)

    await _dialog.message.log(bot=bot, message=f'С канала {ctx.channel.name} удалено {n} сообщений {expLog}')


# Обнуляет символы в статистике, полученные за указанные сообщения
async def delete_exp(MesList):
    defLog: str = ""
    userDict = {}
    # Вычесление удаляемого опыта
    for mes in MesList:
        if mes.author.bot:
            continue

        # Если пользователь попадается впервые, создаётся новый объект
        if mes.author.id not in userDict.keys():
            userDict[mes.author.id] = DBUser(userId=mes.author.id, symbolsCount=0, exp=0, messagesCount=0)

        # Вычисление и запись поинжаемых статистик
        symbolsCount = text_len(mes.content)
        userDict[mes.author.id].symbolsCount -= symbolsCount
        userDict[mes.author.id].exp -= (symbolsCount + 1) / 10
        userDict[mes.author.id].messagesCount -= 1

    # Понижение статистик и логирование
    for authorId in userDict:
        author = userDict[authorId]
        UserService.append_stats_on_messages(user=author)
        defLog += f'\n > {authorId} > удалено: {author.messagesCount} сообщений, ' \
                  f'{author.symbolsCount} символов, {author.exp} опыта'
    return defLog
