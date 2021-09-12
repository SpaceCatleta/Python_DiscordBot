import sqlite3 as sql
from botdb.entities.Gif import Gif

connection: sql.Connection
cursor: sql.Cursor

# ====ADD============================
def add_new_gif_group(gif:  Gif):
    cursor.execute("""
        INSERT INTO gifs (group_id, gif_url)
        VALUES (:groupId, :gifUrl);
        """, gif.__dict__)
    connection.commit()


# ====GET============================
def get_all_gif():
    cursor.execute(""" SELECT * FROM gifs; """)
    return cursor.fetchall()


def get_gif_count_by_group_id(groupId: int):
    cursor.execute("""
        SELECT COUNT(gif_url) FROM gifs
        WHERE group_id = :groupId;
        """, (groupId,))
    return cursor.fetchone()


def get_gif(groupId: int, index: int):
    cursor.execute("""
        SELECT * FROM gifs
        WHERE group_id = :groupId
        LIMIT 1 OFFSET :index;
        """, (groupId, index))
    return cursor.fetchone()


def get_gif_page(groupId: int, index: int):
    cursor.execute("""
        SELECT * FROM gifs
        WHERE group_id = :groupId
        LIMIT 10 OFFSET :index;
        """, (groupId, index))
    return cursor.fetchall()


# ====DELETE============================
def delete_gif(gif: Gif):
    cursor.execute("""
        DELETE FROM gifs
        WHERE group_id = :groupId AND gif_url = :gifUrl;
        """, gif.__dict__)
    connection.commit()

def delete_all_gif_by_group_id(groupId: int):
    cursor.execute("""
        DELETE FROM gifs
        WHERE group_id = :groupId;
        """, (groupId,))
    connection.commit()


def clear_table():
    cursor.execute(""" DELETE FROM gifs; """)
    connection.commit()