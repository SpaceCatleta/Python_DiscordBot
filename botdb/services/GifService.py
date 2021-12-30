import random
from botdb.entities.Gif import Gif
from botdb.repository import GifRep as Repos


# ====ADD============================
# Создаёт новую запись с group_id и gif_url
def add_new_gif(gif:  Gif):
    Repos.add_new_gif_group(gif=gif)


# ====GET============================
# Возвращает все записи из таблицы
def get_all_gif():
    rows = Repos.get_all_gif()
    return [Gif(groupId=row[0], gifUrl=row[1]) for row in rows]


# Возвращает кол-во всех записей с указанным group_id
def get_gif_count_by_group_id(groupId: int):
    return Repos.get_gif_count_by_group_id(groupId=groupId)[0]


# Возвращает кол-во всех записей
def get_all_gif_count():
    return Repos.get_all_gif_count()[0]


# Возвращает одну запись из указанной группы(group_id) и её порядковым номером (определяется порядком хранения в бд)
def get_gif(groupId: int, index: int):
    row = Repos.get_gif(groupId=groupId, index=index - 1)
    if row is None:
        raise ValueError('GifGroupService.get_gif_by_group_id_and_index(): returned row is null')
    return Gif(groupId=row[0], gifUrl=row[1])


# Возвращает 10 записей из указанной группы(group_id) начиная с указанного по пор. (определяется порядком хранения в бд)
def get_gif_page(groupId: int, index: int):
    rows = Repos.get_gif_page(groupId=groupId, index=index - 1)
    answer = []
    for row in rows:
        answer.append(Gif(groupId=row[0], gifUrl=row[1]))
    return answer


# Возвращает одну случайную запись из указанной группы(group_id)
def get_random_gif_from_group(groupId: int):
    size = get_gif_count_by_group_id(groupId=groupId)
    index = random.randint(1, size)
    return get_gif(groupId=groupId, index=index)


# ====DELETE============================
# Удаляет запись по группе(group_id) и её порядковому номеру (определяется порядком хранения в бд)
def delete_gif_by_group_id_and_index(groupId: int, index: int):
    gif = get_gif(groupId=groupId, index=index)
    Repos.delete_gif(gif=gif)


# Удаляет все гиф из указанной группе по group_id
def delete_all_gif_by_group_id(groupId: int):
    Repos.delete_all_gif_by_group_id(groupId=groupId)


# Удаляет все записи из таблицы
def clear_table():
    Repos.clear_table()
