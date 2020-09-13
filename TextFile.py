import structs


def WriteSymbolsStat(filename, statslist):
    file = open(filename, 'w')
    for user in statslist:
        file.write(str(user.id) + ' ' + str(user.counter) + '\n')
    file.close()


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


def RadAll(filename):
    file = open(filename, encoding='utf-8')
    text = file.read()
    return text