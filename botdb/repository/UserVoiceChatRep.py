import sqlite3 as sql
from botdb.entities.UserVoiceChat import UserVoiceChat

connection: sql.Connection
cursor: sql.Cursor


# ====ADD============================
def add_new_user_voice_chat(userVoiceChat: UserVoiceChat):
    cursor.execute("""
        INSERT INTO user_voice_chats (user_id, chat_name)
        VALUES (:userId, :chatName);
        """, userVoiceChat.__dict__)
    connection.commit()


# ====GET============================
def get_user_voice_chat_by_user_id(userId: int):
    cursor.execute("""
        SELECT * FROM user_voice_chats
        WHERE user_id = :userId;
        """, (userId,))
    return cursor.fetchone()


def get_all_user_voice_chats():
    cursor.execute("""SELECT * FROM user_voice_chats """)
    return cursor.fetchall()


# ====UPDATE============================
def update_user_voice_chat(userVoiceChat: UserVoiceChat):
    cursor.execute("""
        UPDATE user_voice_chats SET
        chat_name = :chatName,
        max_users_count = :maxUsersCount
        WHERE user_id = :userId;
        """, userVoiceChat.__dict__)
    connection.commit()


# ====DELETE============================
def delete_user_voice_chat_by_user_id(userId: int):
    cursor.execute("""
        DELETE FROM user_voice_chats
        WHERE user_id = :userId;
        """, (userId,))
    connection.commit()


def clear_table():
    cursor.execute("""DELETE FROM user_voice_chats;""")
    connection.commit()