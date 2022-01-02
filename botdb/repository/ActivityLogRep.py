import sqlite3 as sql
import botdb.database as DB
from datetime import datetime

from botdb.entities.ActivityLog import ActivityLog

# ====ADD============================
def add(entity: ActivityLog):
    connection, cursor = DB.get_connection()
    cursor.execute("""
        INSERT INTO activity_log (guild_id, user_id, period, messages_count, symbols_count, voice_chat_time, spam_messages_count, spam_symbols_count)
        VALUES (:guildId, :userId, :period, :messagesCount, :symbolsCount, :voiceChatTime, :spamMessagesCount, :spamSymbolsCount);
        """, entity.__dict__)

    connection.commit()
    DB.close_connection(connection, cursor)


# ====GET============================
def get_by_primary_key(guildId: int, userId: int, period: datetime.date):
    connection, cursor = DB.get_connection()
    cursor.execute(""" SELECT * FROM activity_log
        WHERE guild_id = :guildId
        AND user_id = :userId
        AND period = :period;
        """, (guildId, userId, period))

    row = cursor.fetchone()
    DB.close_connection(connection, cursor)

    return ActivityLog.from_row(row=row) if row is not None else None


def get_all():
    connection, cursor = DB.get_connection()
    cursor.execute(""" SELECT * FROM activity_log; """)

    rows = cursor.fetchall()
    DB.close_connection(connection, cursor)

    return [ActivityLog.from_row(row=row) for row in rows]


def get_count():
    connection, cursor = DB.get_connection()
    cursor.execute(""" SELECT COUNT(guild_id) FROM activity_log; """)

    answer = cursor.fetchone()[0]
    DB.close_connection(connection, cursor)

    return answer


# ====UPDATE============================
def update(entity: ActivityLog):
    connection, cursor = DB.get_connection()
    cursor.execute("""
        UPDATE activity_log SET
         
        messages_count = :messagesCount,
        symbols_count = :symbolsCount,
        voice_chat_time = :voiceChatTime,
        spam_messages_count = :spamMessagesCount,
        spam_symbols_count = :spamSymbolsCount

        WHERE guild_id = :guildId
        AND user_id = :userId
        AND period = :period;
        """, entity.__dict__)

    connection.commit()
    DB.close_connection(connection, cursor)


# ====DELETE============================
def delete_gif(guildId: int, userId: int, period: datetime.date):
    connection, cursor = DB.get_connection()
    cursor.execute(""" DELETE FROM activity_log
            WHERE guild_id = :guildId,
            AND user_id = userId,
            AND period = :period;
            """, (guildId, userId, period))

    connection.commit()
    DB.close_connection(connection, cursor)


def clear_table():
    connection, cursor = DB.get_connection()
    cursor.execute(""" DELETE FROM activity_log; """)
    connection.commit()
    DB.close_connection(connection, cursor)