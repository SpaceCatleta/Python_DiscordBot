import sqlite3 as sql
from botdb.entities.GifGroup import GifGroup
from botdb.repository import GifGroupRep as Repos


# ====ADD============================
# Записывает id автора, дату создания и название
def add_new_gif_group(gifGroup:  GifGroup):
    Repos.add_new_gif_group(gifGroup=gifGroup)


# Записывает id автора, дату создания, название и фразу
def add_new_gif_group_full(gifGroup:  GifGroup):
    Repos.add_new_gif_group_full(gifGroup=gifGroup)


# ====GET============================
# Проверяет существует ли запись с указанным именем
def is_exist_gif_group_by_name(name: str):
    row: sql.Row = Repos.get_gif_group_by_name(name=name)
    return False if row is None else True


# Проверяет существует ли запись с указанным group_id
def is_exist_gif_group_by_id(groupId: int):
    row: sql.Row = Repos.get_gif_group_by_id(groupId=groupId)
    return False if row is None else True


# Вовзращает все данные из записи по полю group_id
def get_gif_group_by_id(groupId: int):
    row: sql.Row = Repos.get_gif_group_by_id(groupId=groupId)
    if row is None:
        raise ValueError('Ключевое слово с данным id не найдено')
    return GifGroup(groupId=groupId, authorId=row[1], createDate=row[2],
                    accessLevel=row[3], groupType=row[4], name=row[5], phrase=row[6])


# Вовзращает все данные из записи по полю name
def get_gif_group_by_name(name: str):
    row: sql.Row = Repos.get_gif_group_by_name(name=name)
    if row is None:
        raise ValueError('Данное ключевое слово не найдено')
    return GifGroup(groupId=row[0], authorId=row[1], createDate=row[2],
                    accessLevel=row[3], groupType=row[4], name=row[5], phrase=row[6])

# def get_gif_groups_by_type(groupType: str):
#     rows = Repos.get_gif_groups_by_type(groupType=groupType)
#     answer = []
#     for row in rows:
#         answer.append(GifGroup(groupId=row[0], authorId=row[1], createDate=row[2],
#                                accessLevel=row[3], groupType=row[4], name=row[5], phrase=row[6]))
#     return answer


# Возвращает все записи из таблицы
def get_all_gif_groups():
    rows = Repos.get_all_gif_groups()
    answer = []
    for row in rows:
        answer.append(GifGroup(groupId=row[0], authorId=row[1], createDate=row[2],
                               accessLevel=row[3], groupType=row[4], name=row[5], phrase=row[6]))
    return answer


# ====UPDATE============================
# Обновляет все даннные
def update_gif_group(gifGroup:  GifGroup):
    Repos.update_gif_group(gifGroup=gifGroup)


# Обновляет только access_level
def update_gif_group_access_level(gifGroup:  GifGroup):
    Repos.update_gif_group_access_level(gifGroup=gifGroup)


# Обновляет только phrase
def update_gif_group_phrase(gifGroup:  GifGroup):
    Repos.update_gif_group_phrase(gifGroup=gifGroup)


# ====DELETE============================
# удаляет запись по полю group_id
def delete_gif_group_by_id(groupId: int):
    Repos.delete_gif_group_by_id(groupId=groupId)


# удаляет запись по полю name
def delete_gif_group_by_name(name: str):
    Repos.delete_gif_group_by_name(name=name)


# Удаляет все записи таблицы
def clear_table():
    Repos.clear_table()
