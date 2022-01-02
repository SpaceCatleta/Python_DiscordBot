import sqlite3 as sql
from botdb.repository import UserRep, GifGroupRep, GifRep, UserVoiceChatRep, GuildRep, LevelRoleRep, GuildUserRep,\
    QuestionRep, GeneralSettingsRep, SpamChannelsRep

connection: sql.Connection
cursor: sql.Cursor

default_path: str = ""

def open(path: str):
    global connection, cursor
    connection = sql.connect(path)
    cursor = connection.cursor()

    UserRep.connection = connection
    UserRep.cursor = cursor

    GifGroupRep.connection = connection
    GifGroupRep.cursor = cursor

    GifRep.connection = connection
    GifRep.cursor = cursor

    UserVoiceChatRep.connection = connection
    UserVoiceChatRep.cursor = cursor

    GuildRep.connection = connection
    GuildRep.cursor = cursor

    LevelRoleRep.connection = connection
    LevelRoleRep.cursor = cursor

    GuildUserRep.connection = connection
    GuildUserRep.cursor = cursor

    QuestionRep.connection = connection
    QuestionRep.cursor = cursor

    GeneralSettingsRep.connection = connection
    GeneralSettingsRep.cursor = cursor

    SpamChannelsRep.connection = connection
    SpamChannelsRep.cursor = cursor

    print('database: connected - {0}'.format(path))

def get_connection():
    conn =  sql.connect(default_path,detect_types=sql.PARSE_DECLTYPES)
    return conn, conn.cursor()

def close_connection(conn, cursor):
    cursor.close()
    conn.close()

def close():
    connection.close()
    print('database: connection closed')
