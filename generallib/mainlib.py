import discord


# Получает название роли из контекста
# Роль должна быть задана либо линком, либо именем в 3 аргументе
def get_rolename(ctx):
    if len(ctx.message.role_mentions) > 0:
        return ctx.message.role_mentions[0].name
    else:
        arglist = ctx.message.content.split(' ')
        if len(arglist) > 2:
            return arglist[2]
    return None


# Функция рассчёта поулчаемого опыта из сообщения
def mylen(stroke: str):
    counter: int = 0
    iscount: bool = True
    for sym in stroke:
        if sym == '<':
            iscount = False
        elif sym == '>':
            iscount = True
            continue
        if iscount:
            counter += 1
    return counter


# Конвертирует словарь в двумерный список
def DictToList(userdict: dict):
    newlist = []
    for key in userdict:
        newlist.append([key, userdict[key]])
    return newlist


# Выводит словарь на печать
def PrintDict(userdict: dict, delsymb: str = ':'):
    text = ''
    for key in userdict:
        text += '{0}{1}{2}\n'.format(str(key), delsymb, str(userdict[key]))
    return text


# Находит указанную оль в списке
def Findrole(rolelist: list, serchrole: str):
    for curr_role in rolelist:
        if curr_role.name == serchrole:
            return curr_role


# Ищет значение в списке
def is_match(el_list: list, value):
    for element in el_list:
        if value == element:
            return True
    return False

def symbols_in_str(stroke: str, char: str):
    counter = 0
    for symbol in stroke:
        if symbol == char:
            counter += 1
    return counter
