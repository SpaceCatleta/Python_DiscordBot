
def searchid(list, ID: int):
    for stat in list:
        if stat.id == ID:
            return stat
    return None


# Описывает статистику одного пользователя
class userstats(object):
    id: int
    counter: int

    def __init__(self, ID: int, Counter: int):
        self.id = ID
        self.counter = Counter
