import sqlite3 as sql
from botdb.entities.User import User
from botdb.repository import UserRep as Repos


# ====ADD============================
def add_new_user(userId: int):
    Repos.add_new_user(userId=userId)


# ====GET============================
# Вовзращает все записи(со всеми полями) в таблице
def get_all_users():
    answer = []
    for row in Repos.get_all_users():
        answer.append(User(userId=row[0], exp=row[1], level=row[2], messagesCount=row[3],
                           symbolsCount=row[4], voiceChatTime=row[5], voluteCount=row[6], expModifier=row[7]))
    return answer


# Вовзращает все поля пользователя по его user_id
def get_user_by_id(userId: int):
    row: sql.Row = Repos.get_user_by_id(userId=userId)
    if row is None:
        raise ValueError('UserService.get_user_by_id(): returned row is null')
    return User(userId=row[0], exp=row[1], level=row[2], messagesCount=row[3],
                symbolsCount=row[4], voiceChatTime=row[5], voluteCount=row[6], expModifier=row[7])


# Возвращает только необходимые поля пользователя по его user_id
def get_user_on_messages_by_id(userId: int):
    row: sql.Row = Repos.get_user_on_messages_by_id(userId=userId)
    if row is None:
        raise ValueError('UserService.get_user_on_messages_by_id(): returned row is null')
    return User(userId=row[0], exp=row[1],  messagesCount=row[2],  symbolsCount=row[3])


# Возвращает только необходимые поля пользователя по его user_id
def get_user_on_voice_chat_by_id(userId: int):
    row: sql.Row = Repos.get_user_on_voice_chat_by_id(userId=userId)
    if row is None:
        raise ValueError('UserService.get_user_on_voice_chat_by_id(): returned row is null')
    return User(userId=row[0], exp=row[1], voiceChatTime=row[2])


# Возвращает только необходимые поля пользователя по его user_id
def get_user_exp_modifier(userId: int):
    row: sql.Row = Repos.get_user_exp_modifier(userId=userId)
    if row is None:
        raise ValueError('UserService.get_user_expModifier(): returned row is null')
    return User(userId=row[0], exp=row[1], expModifier=row[2])


def get_top10_by_exp():
    rows = Repos.get_top10_by_exp()
    if rows is None:
        raise ValueError('UserService.get_top10_by_exp(): returned rows is null')
    answer = []
    for row in rows:
        answer.append(User(userId=row[0], exp=row[1], level=row[2], messagesCount=row[3],
                           symbolsCount=row[4], voiceChatTime=row[5], voluteCount=row[6], expModifier=row[7]))
    return answer

# ====UPDATE============================
# Обновляет все поля пользователя
def update_user(user: User):
    Repos.update_user(user=user)


# Обновляет только поля exp, messages_count и symbol_count пользователя
def append_stats_on_messages(user: User):
    append_stats_on_messages2(user.userId, exp=user.exp, messagesCount=user.messagesCount,
                              symbolsCount=user.symbolsCount)


# Обновляет только поля exp, messages_count и symbol_count пользователя
def append_stats_on_messages2(userId: int, exp: float, messagesCount: int, symbolsCount: int):
    baseUser: User = get_user_on_messages_by_id(userId=userId)
    baseUser.exp += exp
    baseUser.messagesCount += messagesCount
    baseUser.symbolsCount += symbolsCount
    Repos.update_user_on_messages(userId=baseUser.userId, exp=baseUser.exp, messagesCount=baseUser.messagesCount,
                                  symbolsCount=baseUser.symbolsCount)


# Обновляет только поля exp, messages_count и symbol_count пользователя
def append_stats_on_messages_with_level_check(userId: int, exp: float, mesCount: int, symbolsCount: int, funcX):
    baseUser: User = get_user_on_messages_by_id(userId=userId)
    old_level = funcX(baseUser.exp)
    baseUser.exp += exp
    baseUser.messagesCount += mesCount
    baseUser.symbolsCount += symbolsCount

    Repos.update_user_on_messages(userId=baseUser.userId, exp=baseUser.exp, messagesCount=baseUser.messagesCount,
                                  symbolsCount=baseUser.symbolsCount)
    new_level = funcX(baseUser.exp)
    return True if new_level != old_level else False


# Обновляет только поля exp и voice_chat_time пользователя
def append_stats_on_voice_chat(user: User):
    append_stats_on_voice_chat2(userId=user.userId, exp=user.exp, voiceChatTime=user.voiceChatTime)


# Обновляет только поля exp и voice_chat_time пользователя
def append_stats_on_voice_chat2(userId: int, exp: float, voiceChatTime: int):
    baseUser: User = get_user_on_voice_chat_by_id(userId=userId)
    baseUser.exp += exp
    baseUser.voiceChatTime += voiceChatTime
    Repos.update_user_on_voice_chat(userId=baseUser.userId, exp=baseUser.exp, voiceChatTime=baseUser.voiceChatTime)


# Обновляет только поле level пользователя
def update_user_level(user: User):
    update_user_level2(userId=user.userId, level=user.level)


# Обновляет только поле level пользователя
def update_user_level2(userId: int, level: int):
    Repos.update_user_level(userId=userId, level=level)


# Обновляет только поля exp_modifier и exp пользователя
def add_user_exp_modifier(user: User):
    add_user_exp_modifier2(userId=user.userId, exp=user.exp, expModifier=user.expModifier)


# Обновляет только поля exp_modifier и exp пользователя
def add_user_exp_modifier2(userId: int, exp: float, expModifier: int):
    baseUser: User = get_user_exp_modifier(userId=userId)
    baseUser.exp += exp
    baseUser.expModifier += expModifier
    Repos.update_user_exp_modifier(userId=baseUser.userId, exp=baseUser.exp, expModifier=baseUser.expModifier)


# ====DELETE============================
# Вовзращает все поля пользователя по его user_id
def delete_user_by_id(userId: int):
    Repos.delete_user_by_id(userId=userId)


# Удаляет все записи в таблице
def clear_table():
    Repos.clear_table()
