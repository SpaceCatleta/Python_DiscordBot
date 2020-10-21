from structs import userstats


# Содержит в себе список usersats и методы для него
class UserStatsList(object):
    # кол-во элементов списка
    count: int = 0
    # список
    UsersStats = []

    # конструктор
    def __init__(self):
        self.count = 0
        self.UsersStats = []

    # итератор
    def __iter__(self):
        return iter(self.UsersStats)

    # получение по индексу
    def __getitem__(self, item):
        return self.UsersStats[item]

    # добавление элемента в конец списка
    def push(self, item: userstats.userstats):
        self.UsersStats.append(item)
        self.count += 1

    # изъятие элемента из списка по индексу
    def pop(self, index: int = count - 1):
        self.count -= 1
        return self.UsersStats.pop(index)

    # изъятие элемента из списка по ID
    def pop_by_id(self, ID: int):
        length = len(self.UsersStats)
        for i in range(0, length):
            if self.UsersStats[i].id == ID:
                return self.pop(i)
        return -1

    # поиск по ID
    def search_id(self, ID: int):
        for stats in self.UsersStats:
            if stats.id == ID:
                return stats
        return None

    # Слияние с другим списком
    def merge_with(self, newlist):
        for stat in newlist:
            stat1 = self.search_id(stat.id)
            if stat1 is not None:
                stat1.add(stat)
            else:
                self.push(stat)

    # слияние с другим списком с заменой
    def replace_stats(self, stats_addend):
        for i in range(self.count):
            stat2 = stats_addend.search_id(self.UsersStats[i].id)
            if stat2 is not None:
                self.UsersStats[i] = stat2
            else:
                self.UsersStats[i].clear()
