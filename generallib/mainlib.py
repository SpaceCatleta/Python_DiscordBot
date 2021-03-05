

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
