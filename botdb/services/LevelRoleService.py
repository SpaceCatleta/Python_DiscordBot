from botdb.entities.LevelRole import LevelRole
from botdb.repository import LevelRoleRep as Repos


# ====ADD============================
def add_level_role(levelRole: LevelRole):
    Repos.add_level_role(levelRole=levelRole)


# ====GET============================
def get_all_level_roles():
    rows = Repos.get_all_level_roles()
    return [LevelRole(guildId=row[0], level=row[1], roleId=row[2]) for row in rows]


def get_level_roles_dict_by_guild_id(guildId: int):
    rows = Repos.get_level_roles_dict_by_guild_id(guildId=guildId)
    return {row[1]: LevelRole(guildId=row[0], level=row[1], roleId=row[2]) for row in rows}


def get_all_level_roles_count():
    return Repos.get_all_level_roles_count()[0]


def get_level_roles_count_by_guild_id(guildId: int):
    return Repos.get_level_roles_count_by_guild_id(guildId=guildId)[0]


# ====UPDATE============================
def update_level_role(levelRole: LevelRole):
    Repos.update_level_role(levelRole=levelRole)


# ====DELETE============================
def delete_level_role(levelRole: LevelRole):
    Repos.delete_level_role(levelRole=levelRole)

def delete_level_role_by_guild_id_and_level(guildId: int, level: int):
    delete_level_role(LevelRole(guildId=guildId, level=level, roleId=None))

def delete_level_roles_by_guild_id(guildId: int):
    Repos.delete_level_roles_by_guild_id(guildId=guildId)


def clear_table():
    Repos.clear_table()