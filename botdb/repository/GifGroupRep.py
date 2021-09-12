import sqlite3 as sql
from botdb.entities.GifGroup import GifGroup

connection: sql.Connection
cursor: sql.Cursor


# ====ADD============================
def add_new_gif_group(gifGroup:  GifGroup):
    cursor.execute("""
        INSERT INTO gif_groups (author_id, create_date, name)
        VALUES (:authorId, :createDate, :name);
        """, gifGroup.__dict__)
    connection.commit()


def add_new_gif_group_full(gifGroup:  GifGroup):
    cursor.execute("""
        INSERT INTO gif_groups (author_id, create_date, name, phrase)
        VALUES (:authorId, :createDate, :name, :phrase);
        """, gifGroup.__dict__)
    connection.commit()


# ====GET============================
def get_gif_group_by_id(groupId: int):
    cursor.execute("""
        SELECT * from gif_groups
        WHERE group_id = :groupId;
        """, (groupId,))
    return cursor.fetchone()


def get_gif_group_by_name(name: str):
    cursor.execute("""
        SELECT * from gif_groups
        WHERE name = :name;
        """, (name,))
    return cursor.fetchone()

# def get_gif_groups_by_type(groupType: str):
#     cursor.execute("""
#         SELECT * from gif_groups
#         WHERE group_type = 'common'
#         """)


def get_all_gif_groups():
    cursor.execute(""" SELECT * from gif_groups; """)
    return cursor.fetchall()


# ====UPDATE============================
def update_gif_group(gifGroup:  GifGroup):
    cursor.execute("""
        UPDATE gif_groups SET
        author_id = :authorId,
        create_date = :createDate,
        name = :name,
        phrase = :phrase,
        access_level = :accessLevel,
        group_type = :groupType
        WHERE group_id = :groupId;
        """, gifGroup.__dict__)
    connection.commit()


def update_gif_group_access_level(gifGroup:  GifGroup):
    cursor.execute("""
        UPDATE gif_groups SET
        access_level = :accessLevel
        WHERE group_id = :groupId;
        """, gifGroup.__dict__)
    connection.commit()


def update_gif_group_phrase(gifGroup:  GifGroup):
    cursor.execute("""
        UPDATE gif_groups SET
        phrase = :phrase
        WHERE group_id = :groupId;
        """, gifGroup.__dict__)
    connection.commit()


# ====DELETE============================
def delete_gif_group_by_id(groupId: int):
    cursor.execute("""
        DELETE FROM gif_groups
        WHERE group_id = :groupId;
        """, (groupId,))
    connection.commit()


def delete_gif_group_by_name(name: str):
    cursor.execute("""
        DELETE FROM gif_groups
        WHERE name = :name;
        """, (name,))
    connection.commit()


def clear_table():
    cursor.execute(""" DELETE FROM gif_groups; """)
    cursor.execute(""" UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='gif_groups'; """)
    connection.commit()
