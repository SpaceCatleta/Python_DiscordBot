import sqlite3 as sql
from botdb.entities.GuildMember import GuildMember

connection: sql.Connection
cursor: sql.Cursor


# ====ADD============================
def add_guild_member(guildMember: GuildMember):
    cursor.execute("""
        INSERT INTO guilds_members (user_id, guild_id)
        VALUES (:userId, :guildId);
        """, guildMember.__dict__)
    connection.commit()


# ====GET============================
def get_guild_member_by_ids(userId: int, guildId: int):
    cursor.execute("""
        SELECT * FROM guilds_members
        WHERE user_id = :userId
        AND guild_id = :guildId;
        """, (userId, guildId))
    return cursor.fetchone()


def get_all_guild_members():
    cursor.execute(""" SELECT * FROM guilds_members; """)
    return cursor.fetchall()


def get_members_count():
    cursor.execute(""" SELECT COUNT(guild_id) FROM guilds_members; """)
    return cursor.fetchone()


def get_members_count_by_guild_id(guildId):
    cursor.execute("""
        SELECT COUNT(guild_id) FROM guilds_members
        WHERE guild_id = :guildId;
        """, (guildId,))
    return cursor.fetchone()


# ====UPDATE============================
def update_guild_member(guildMember: GuildMember):
    cursor.execute("""
        UPDATE guilds_members SET
        visits_count = :visitsCount,
        warnings_count = :warningsCount,
        ban_bot_functions = :banBotFunctions,
        personal_role_id = :personalRoleId,
        punishment_role_id = :punishmentRoleId,
        punishment_end_date = :punishmentEndDate
        WHERE user_id = :userId
        AND guild_id = :guildId;
        """, guildMember.__dict__)
    return cursor.fetchone()


def update_guild_member_personal_role(guildMember: GuildMember):
    cursor.execute("""
        UPDATE guilds_members SET
        personal_role_id = :personalRoleId
        WHERE user_id = :userId
        AND guild_id = :guildId;
        """, guildMember.__dict__)
    return cursor.fetchone()


def update_guild_member_ban_func(guildMember: GuildMember):
    cursor.execute("""
        UPDATE guilds_members SET
        ban_bot_functions = :banBotFunctions
        WHERE user_id = :userId
        AND guild_id = :guildId;
        """, guildMember.__dict__)
    return cursor.fetchone()


def update_guild_member_punishment(guildMember: GuildMember):
    cursor.execute("""
        UPDATE guilds_members SET
        punishment_role_id = :punishmentRoleId,
        punishment_end_date = :punishmentEndDate
        WHERE user_id = :userId
        AND guild_id = :guildId;
        """, guildMember.__dict__)
    return cursor.fetchone()

# ====DELETE============================
def delete_guild_member_by_ids(userId: int, guildId: int):
    cursor.execute("""
        DELETE FROM guilds_members
        WHERE user_id = :userId
        AND guild_id = :guildId;
        """, (userId, guildId))
    connection.commit()


def delete_guild_members_guild_id(guildId: int):
    cursor.execute("""
        DELETE FROM guilds_members
        WHERE guild_id = :guildId;
        """, (guildId,))
    connection.commit()


def clear_table():
    cursor.execute(""" DELETE FROM guilds_members; """)
    connection.commit()