import discord

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


def get_role(ctx, bufferParts: int = 1):
    if len(ctx.message.role_mentions) > 0:
        return ctx.message.role_mentions[0]
    else:
        argList = ctx.message.content.split(' ')
        roleName = ' '.join(argList[bufferParts:])
        if len(argList) > bufferParts:
            answer = discord.utils.get(iterable=ctx.guild.roles, name=roleName)
            if answer is None:
                raise ValueError('{0} - название роли указано неверно'.format(roleName))
            return answer
    return None


def get_user_link(ctx):
    if len(ctx.message.mentions) > 0:
        return ctx.message.mentions[0]
    else:
        raise ValueError('Не указан пользователь')


def get_text_chat_link(ctx):
    print('======')
    for ch in ctx.message.channel_mentions:
        print(ch)
    print('======')
    if len(ctx.message.channel_mentions) > 0:
        return ctx.message.channel_mentions[0]
    else:
        raise ValueError('Не указан канал')