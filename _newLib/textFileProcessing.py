
# Читает всё из указанного файла
def RadAll(filename):
    with open(filename, encoding='utf-8') as TF:
        return TF.read()