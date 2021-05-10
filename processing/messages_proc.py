

# Функция рассчёта количества символов без учёта эмодзи
def text_len(stroke: str):
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


# вовзращает кол-во появлений символа в тексте
def symbols_in_text(stroke: str, char: str):
    counter = 0
    for symbol in stroke:
        if symbol == char:
            counter += 1
    return counter


def get_rolename(ctx):
    if len(ctx.message.role_mentions) > 0:
        return ctx.message.role_mentions[0].name
    else:
        arglist = ctx.message.content.split(' ')
        if len(arglist) > 2:
            return arglist[2]
    return None


def is_gif(message):
    length = len(message.content)
    if message.content[0:8] == 'https://':
        return True
    else:
        return False
