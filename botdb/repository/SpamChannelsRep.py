import sqlite3 as sql
from botdb.entities.SpamChannel import SpamChannel

connection: sql.Connection
cursor: sql.Cursor


# ====ADD============================
def add(spamChannel: SpamChannel):
    cursor.execute("""
        INSERT INTO spam_channels (guild_id, channel_id)
        VALUES (:guildId, :channelId);
        """, spamChannel.__dict__)
    connection.commit()


# ====GET============================

def get_by_id(guildId: int, channelId: int):
    cursor.execute("""
            SELECT * FROM spam_channels
            WHERE guild_id = :guildId
            AND channel_id = :channelId;
            """, (guildId, channelId))
    row = cursor.fetchone()
    return SpamChannel(guildId=row[0], channelId=row[1]) if row is not None else None


def get_by_guild_id(guildId: int):
    cursor.execute("""
        SELECT * FROM spam_channels
        WHERE guild_id = :guildId;
        """, (guildId,))
    return [SpamChannel(guildId=row[0], channelId=row[1]) for row in cursor.fetchall()]

def get_id_list_by_guild_id(guildId: int):
    cursor.execute("""
        SELECT channel_id FROM spam_channels
        WHERE guild_id = :guildId;
        """, (guildId,))
    return [row[0] for row in cursor.fetchall()]


def get_count():
    cursor.execute(""" SELECT COUNT(guild_id) FROM spam_channels; """)
    return cursor.fetchone()[0]


def get_all():
    cursor.execute(""" SELECT * FROM spam_channels; """)
    return [SpamChannel(guildId=row[0], channelId=row[1]) for row in cursor.fetchall()]


# ====DELETE============================
def delete_by_id(guildId: int, channelId: int):
    cursor.execute("""
        DELETE FROM spam_channels
        WHERE guild_id = :guildId
        AND channel_id = :channelId;
        """, (guildId, channelId))
    connection.commit()


def clear_table():
    cursor.execute(""" DELETE FROM spam_channels; """)
    connection.commit()
