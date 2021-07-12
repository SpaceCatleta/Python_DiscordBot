import discord
from mycommands import dilogcomm

stop_exe: bool = False

# спам линком в чате
async def bomb(ctx: discord.ext.commands.Context, text: str = ''):
    mes = ctx.message
    if len(mes.mentions) > 0:
        link = mes.mentions[0]
    elif len(mes.role_mentions) > 0:
        link = mes.role_mentions[0]
    else:
        return
    for i in range(1, 11):
        if stop_exe == True:
            await ctx.send('```выполнение прервано```')
            return -2
        await ctx.send('[{0}] '.format(i) + link.mention + ' ' + text)
    return 0

# находит упоминание в сообщении и вовзращает его ник
def get_name_from_mention(message):
    if len(message.mentions) > 0:
        return message.mentions[0].name
    elif len(message.role_mentions) > 0:
        return message.role_mentions[0].name
    else:
        return 'None'

# возвращает список параметром замещая линк ником (работает только с одним ником)
def create_params_list_removing_links_to_str(message):
    answer = []
    link = None
    if len(message.mentions) > 0:
        link =  message.mentions[0].name

    for word in message.content.split(' '):
        if '@' in word:
            answer.append(link)
        else:
            answer.append(word.replace('-', ''))

    return answer


# создаёт список параметров и извлекает из него линки
def extract_links_from_params_list(message):
    answer = []
    link = None
    if len(message.mentions) > 0:
        link = message.mentions[0].name

    for word in message.content.split(' '):
        if '@' in word:
            pass
        else:
            w = word.replace('-', '')
            if w == '':
                continue
            answer.append(w)

    return answer, link
