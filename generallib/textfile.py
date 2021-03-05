from generallib import mainlib


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
def ReadParams(filename: str, delsymb: str = ':'):
    file = open(filename, encoding='utf-8')
    parlist = []
    for line in file:
        line = line.replace('\n', '')
        try:
            stroke = line.split(delsymb)
            if len(stroke) < 2:
                break
            parlist.append([stroke[0], stroke[1]])
        except ValueError:
            print('one read error')
    file.close()
    return parlist


# записывает параметры в указанный файл
def WriteParams(ParamsDict: dict, filename: str, delsymb: str = ':'):
    file = open(filename, 'w', encoding='utf-8')
    file.write(mainlib.PrintDict(ParamsDict, delsymb=delsymb))
    file.close()
