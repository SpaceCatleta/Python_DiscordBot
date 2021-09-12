import sqlite3 as sql
from botdb.repository import UserRep, GifGroupRep, GifRep, UserVoiceChatRep, GuildRep, LevelRoleRep, GuldMemberRep,\
    QuestionRep, GeneralSettingsRep

connection: sql.Connection
cursor: sql.Cursor


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

    GuldMemberRep.connection = connection
    GuldMemberRep.cursor = cursor

    QuestionRep.connection = connection
    QuestionRep.cursor = cursor

    GeneralSettingsRep.connection = connection
    GeneralSettingsRep.cursor = cursor

    print('database: connected - {0}'.format(path))


def close():
    connection.close()
    print('database: connection closed')
