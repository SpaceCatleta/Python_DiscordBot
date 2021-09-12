import sqlite3 as sql
from botdb.entities.LevelRole import LevelRole

connection: sql.Connection
cursor: sql.Cursor


# ====ADD============================
def add_level_role(levelRole: LevelRole):
    cursor.execute("""
        INSERT INTO level_roles (guild_id, level, role_id)
        VALUES (:guildId, :level, :roleId);
        """, levelRole.__dict__)
    connection.commit()


# ====GET============================
def get_level_roles_dict_by_guild_id(guildId: int):
    cursor.execute("""
        SELECT * FROM level_roles
        WHERE guild_id = :guildId;
        """, (guildId,))
    return cursor.fetchall()


def get_all_level_roles():
    cursor.execute(""" SELECT * FROM level_roles; """)
    return cursor.fetchall()


def get_all_level_roles_count():
    cursor.execute(""" SELECT COUNT(guild_id) FROM level_roles; """)
    return cursor.fetchone()


def get_level_roles_count_by_guild_id(guildId: int):
    cursor.execute("""
        SELECT COUNT(guild_id) FROM level_roles
        WHERE guild_id = :guildId;
    """, (guildId,))
    return cursor.fetchone()


# ====UPDATE============================
def update_level_role(levelRole: LevelRole):
    cursor.execute("""
        UPDATE level_roles SET
        role_id = :roleId
        WHERE guild_id = :guildId
        AND level = :level;
        """, levelRole.__dict__)
    connection.commit()


# ====DELETE============================
def delete_level_role(levelRole: LevelRole):
    cursor.execute("""
        DELETE FROM level_roles
        WHERE guild_id = :guildId
        AND level = :level;
        """, levelRole.__dict__)
    connection.commit()


def delete_level_roles_by_guild_id(guildId: int):
    cursor.execute("""
        DELETE FROM level_roles
        WHERE guild_id = :guildId;
        """, (guildId,))
    connection.commit()


def clear_table():
    cursor.execute(""" DELETE FROM level_roles; """)
    connection.commit()
