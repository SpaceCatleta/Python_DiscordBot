from generallib import structs, mainlib


# записывет данные о статистике напечатанных символов в указаннный файл
def WriteSymbolsStat(filename, statslist):
    file = open(filename, 'w')
    for user in statslist:
        file.write('{0} {1}|{2}|{3}|{4}|{5}\n'.format(str(user.id),
                                                      str(user.exp),
                                                      str(user.lvl),
                                                      str(user.mes_counter),
                                                      str(user.symb_counter),
                                                      str(user.vc_counter)))
    file.close()


# читает данные о статистике напечатанных символов из указаннго файла
def ReadSymbolsStat(filename):
    file = open(filename, 'r')
    srlist = []
    for line in file:
        stroke = str(line).split(" ")
        statstr = stroke[1].split('|')
        statuser = structs.userstats(ID=int(stroke[0]), Exp=float(statstr[0]), Lvl=int(statstr[1]), MesCounter=int(statstr[2]), SymbCounter=int(statstr[3]), VCCounter=float(statstr[4]))
        srlist.append(statuser)

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
