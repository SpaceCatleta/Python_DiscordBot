from generallib import structs, mainlib


# записывет данные о статистике напечатанных символов в указаннный файл
def WriteSymbolsStat(filename, statslist):
    file = open(filename, 'w')
    for user in statslist:
        file.write(str(user.id) + ' ' + str(user.counter) + '\n')
    file.close()


# читает данные о статистике напечатанных символов из указаннго файла
def ReadSymbolsStat(filename):
    file = open(filename, 'r')
    srlist = []
    for line in file:
        try:
            stroke = str(line).split(" ")
            srlist.append(structs.userstats(int(stroke[0]), int(stroke[1])))
        except ValueError:
            print('one read error')
    file.close()
    return srlist


# Читает всё из указанного файла
def RadAll(filename):
    file = open(filename, encoding='utf-8')
    text = file.read()
    file.close()
    return text


# записывает текст в указанный файл
def writeAll(filename, text: str):
    file = open(filename, 'w')
    text = file.write(text)
    file.close()


# читает параметры из указанного файла
def ReadParams(filename: str):
    file = open(filename, encoding='windows-1251')
    parlist = []
    for line in file:
        line = line.replace('\n', '')
        try:
            stroke = line.split(':')
            if len(stroke) < 2:
                break
            parlist.append([stroke[0], stroke[1]])
        except ValueError:
            print('one read error')
    file.close()
    return parlist


# записывает параметры в указанный файл
def WriteParams(ParamsDict: dict, filename: str):
    file = open(filename, 'w', encoding='windows-1251')
    file.write(mainlib.PrintDict(ParamsDict))
    file.close()