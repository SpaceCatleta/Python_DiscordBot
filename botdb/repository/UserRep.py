import sqlite3 as sql
from botdb.entities.User import User

connection: sql.Connection
cursor: sql.Cursor


# ====ADD============================
def add_new_user(userId: int):
    cursor.execute("""
        INSERT INTO users (user_id)
        VALUES (:userId);
        """, (userId,))
    connection.commit()


# ====GET============================
def get_all_users():
    cursor.execute(""" SELECT * FROM users; """)
    return cursor.fetchall()


def get_user_by_id(userId: int):
    cursor.execute("""
        SELECT * from users
        WHERE user_id = :userId;
        """, (userId,))
    return cursor.fetchone()


def get_user_on_messages_by_id(userId: int):
    cursor.execute("""
        SELECT user_id, exp, messages_count, symbols_count
        FROM users
        WHERE user_id = :userId;
        """, (userId,))
    return cursor.fetchone()


def get_user_on_voice_chat_by_id(userId: int):
    cursor.execute("""
        SELECT user_id, exp, voice_chat_time
        FROM users
        WHERE user_id = :userId;
        """, (userId,))
    return cursor.fetchone()


def get_user_exp_modifier(userId: int):
    cursor.execute("""
        SELECT user_id, exp, exp_modifier
        FROM users
        WHERE user_id = :userId;
        """, (userId,))
    return cursor.fetchone()


def get_top10_by_exp():
    cursor.execute("""
        SELECT * FROM users
        ORDER BY exp DESC
        LIMIT 10; """)
    return cursor.fetchall()


# ====UPDATE============================
def update_user(user: User):
    cursor.execute("""
        UPDATE users SET
        exp = :exp,
        level = :level,
        messages_count = :messagesCount,
        symbols_count = :symbolsCount,
        voice_chat_time = :voiceChatTime,
        volute_count = :voluteCount,
        exp_modifier = :expModifier
        WHERE user_id = :userId;
        """, user.__dict__)
    connection.commit()


def update_user_on_messages(userId: int, exp: float, messagesCount: int, symbolsCount: int):
    cursor.execute("""
        UPDATE users SET
        exp = :exp,
        messages_count = :messagesCount,
        symbols_count = :symbolsCount
        WHERE user_id = :userId;
        """, (exp, messagesCount, symbolsCount, userId))
    connection.commit()


def update_user_on_voice_chat(userId: int, exp: float, voiceChatTime: int):
    cursor.execute("""
        UPDATE users SET
        exp = :exp,
        voice_chat_time = :voiceChatTime
        WHERE user_id = :userId;
        """, (exp, voiceChatTime, userId))
    connection.commit()


def update_user_level(userId: int, level: int):
    cursor.execute("""
        UPDATE users SET
        level = :level
        WHERE user_id = :userId;
        """, (level, userId))
    connection.commit()


def update_user_exp_modifier(userId: int, exp: float, expModifier: int):
    cursor.execute("""
        UPDATE users SET
        exp = :exp,
        exp_modifier = :expModifier
        WHERE user_id = :userId;
        """, (exp, expModifier, userId))
    connection.commit()


# ====DELETE============================
def delete_user_by_id(userId: int):
    cursor.execute("""
        DELETE FROM users
        WHERE user_id = :userId;
        """, (userId,))
    connection.commit()


def clear_table():
    cursor.execute(""" DELETE FROM users; """)
    connection.commit()
