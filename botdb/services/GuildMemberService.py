from datetime import datetime as DateTime
from botdb.entities.GuildMember import GuildMember
from botdb.repository import GuldMemberRep as Repos


# ====ADD============================
# Добавляет нового члена сервера (заполняет только id)
def add_guild_member(guildMember: GuildMember):
    Repos.add_guild_member(guildMember=guildMember)


# ====GET============================
# Ввзвращает все данные члена сервера по id
def get_guild_member_by_ids(userId: int, guildId: int):
    row = Repos.get_guild_member_by_ids(userId=userId, guildId=guildId)
    if row is None:
        raise ValueError('GuildMemberService.get_guild_member_by_ids(): returned row is null')
    return GuildMember(userId=row[0], guildId=row[1], visitsCount=row[2], warningsCount=row[3],
                       banBotFunctions=row[4], personalRoleId=row[5], punishmentRoleId=row[6],
                       punishmentEndDate= None if row[7] is None else DateTime.strptime(row[7], "%Y-%m-%d %H:%M:%S"))


# Возвращает всех членов сервера
def get_all_guild_members():
    rows = Repos.get_all_guild_members()
    answer = []
    for row in rows:
        answer.append(GuildMember(userId=row[0], guildId=row[1], visitsCount=row[2], warningsCount=row[3],
                                  banBotFunctions=row[4], personalRoleId=row[5], punishmentRoleId=row[6],
                                  punishmentEndDate= None if row[7] is None else DateTime.strptime(row[7], "%Y-%m-%d %H:%M:%S")))

    return answer


# Вовзращает общее кол-во записей в таблице
def get_members_count():
    return Repos.get_members_count()[0]


# Возвращает кол-во членов конкретного сервера, по его id
def get_members_count_by_guild_id(guildId):
    return Repos.get_members_count_by_guild_id(guildId=guildId)[0]


# ====UPDATE============================
# Обновляет все поля по id
def update_guild_member(guildMember: GuildMember):
    Repos.update_guild_member(guildMember=guildMember)


# Обновляет поле member_personal_role_id по id
def update_guild_member_personal_role(guildMember: GuildMember):
    Repos.update_guild_member_personal_role(guildMember=guildMember)


# обновляет поле bot_ban_functions по id (поле принимает значение только 1 или 0)
def update_guild_member_ban_func(guildMember: GuildMember):
    Repos.update_guild_member_ban_func(guildMember=guildMember)


# обновляет только поля punishment_role_id и punishment_end_date
def update_guild_member_punishment(guildMember: GuildMember):
    Repos.update_guild_member_punishment(guildMember=guildMember)


# ====DELETE============================
# Удаляет члена севрера по id
def delete_guild_member_by_ids(userId: int, guildId: int):
    Repos.delete_guild_member_by_ids(userId=userId, guildId=guildId)


# Удаляет всех членов одного сервера по его id
def delete_guild_members_guild_id(guildId: int):
    Repos.delete_guild_members_guild_id(guildId=guildId)


# Удаляет все запси в таблице
def clear_table():
    Repos.clear_table()
