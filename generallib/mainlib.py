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


# Выводит на печать дробное число
def print_number(number: float, number_count):
    main_part = int(number)
    float_part = int(round((number - main_part) * pow(10, number_count), 1))
    return '{0}.{1}'.format(main_part, float_part)


# Конвертирует словарь в двумерный список
def DictToList(userdict: dict):
    newlist = []
    for key in userdict:
        newlist.append([key, userdict[key]])
    return newlist


# Выводит словарь на печать
def PrintDict(userdict: dict):
    text = ''
    for key in userdict:
        text += '{0}:{1}\n'.format(str(key), str(userdict[key]))
    return text


# Находит указанную оль в списке
def Findrole(rolelist: list, serchrole: str):
    for curr_role in rolelist:
        if curr_role.name == serchrole:
            return curr_role
