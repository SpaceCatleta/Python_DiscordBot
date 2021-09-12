import sqlite3 as sql
from botdb.entities.Guild import Guild

connection: sql.Connection
cursor: sql.Cursor


# ====ADD============================
def init_new_guild(guildId: int):
    cursor.execute("""
        INSERT INTO guilds (guild_id)
        VALUES (:guildId)
        """, (guildId,))
    connection.commit()


# ====GET============================
def get_guild_by_guild_id(guildId: int):
    cursor.execute("""
        SELECT * FROM guilds
        WHERE guild_id = :guildId;
        """, (guildId,))
    return cursor.fetchone()


def get_all_guilds():
    cursor.execute(""" SELECT * FROM guilds; """)
    return cursor.fetchall()


def get_guilds_count():
    cursor.execute(""" SELECT COUNT(guild_id) FROM guilds; """)
    return cursor.fetchone()


# ====UPDATE============================
def update_guild_full(guild: Guild):
    cursor.execute("""
        UPDATE guilds SET
        max_links = :maxLinks,
        mute_time = :muteTime,
        personal_roles_allowed = :personalRolesAllowed, 
        ban_bot_functions = :banBotFunctions,
        no_links_role_id = :noLinksRoleId,
        light_mute_role_id = :lightMuteRoleId,
        mute_role_id = :muteRoleId,
        mute_voice_chat_role_id = :muteVoiceChatRoleId,
        CHIELD_chat_id = :CHIELDChatId,
        CHIELD_warning_count = :CHIELDWarningCount,
        CHIELD_alert_count = :CHIELDAlertCount,
        voice_chat_creator_id = :voiceChatCreatorId,
        members_counter_chat_id = :membersCounterChatId,
        roles_counter_chat_id = :rolesCounterChatId,
        welcome_phrase = :welcomePhrase,
        welcome_gif_group_id = :welcomeGifGroupId
        WHERE guild_id = :guildId;
        """, guild.__dict__)
    connection.commit()


def update_guild_common(guild: Guild):
    cursor.execute("""
        UPDATE guilds SET
        max_links = :maxLinks,
        mute_time = :muteTime,
        personal_roles_allowed = :personalRolesAllowed
        WHERE guild_id = :guildId;
        """, guild.__dict__)
    connection.commit()


def update_guild_roles(guild: Guild):
    cursor.execute("""
        UPDATE guilds SET
        ban_bot_functions = :banBotFunctions,
        no_links_role_id = :noLinksRoleId,
        light_mute_role_id = :lightMuteRoleId,
        mute_role_id = :muteRoleId,
        mute_voice_chat_role_id = :muteVoiceChatRoleId
        WHERE guild_id = :guildId;
        """, guild.__dict__)
    connection.commit()


def update_guild_shield_settings(guild: Guild):
    cursor.execute("""
        UPDATE guilds SET
        CHIELD_chat_id = :CHIELDChatId,
        CHIELD_warning_count = :CHIELDWarningCount,
        CHIELD_alert_count = :CHIELDAlertCount
        WHERE guild_id = :guildId;
        """, guild.__dict__)
    connection.commit()


def update_guild_chats(guild: Guild):
    cursor.execute("""
        UPDATE guilds SET
        voice_chat_creator_id = :voiceChatCreatorId,
        members_counter_chat_id = :membersCounterChatId,
        roles_counter_chat_id = :rolesCounterChatId
        WHERE guild_id = :guildId;
        """, guild.__dict__)
    connection.commit()


def update_guild_welcome_phrase(guild: Guild):
    cursor.execute("""
        UPDATE guilds SET
        welcome_phrase = :welcomePhrase
        WHERE guild_id = :guildId;
        """, guild.__dict__)
    connection.commit()


def update_welcome_gif_group_id(guild: Guild):
    cursor.execute("""
        UPDATE guilds SET
        welcome_gif_group_id = :welcomeGifGroupId
        WHERE guild_id = :guildId;
        """, guild.__dict__)
    connection.commit()


# ====DELETE============================
def delete_guild_by_guild_id(guildId: int):
    cursor.execute("""
        DELETE FROM guilds
        WHERE guild_id = ?;
        """, (guildId,))
    connection.commit()


def clear_table():
    cursor.execute(""" DELETE FROM guilds; """)
    connection.commit()
