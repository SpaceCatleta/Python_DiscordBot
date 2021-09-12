import botdb
import sqlite3 as sql
from botdb.services import UserService, GifGroupService, GifService
from botdb.entities.User import User
from botdb.entities.GifGroup import GifGroup
from botdb.entities.Gif import Gif
from datetime import datetime


connection: sql.Connection
cursor: sql.Cursor

basePath = str(botdb)
basePath = basePath.split("'")[-2]
path1 = basePath.split('\\\\')[:-1] + ['transfer'] + ['botdata.db']
path1 = '\\\\'.join(path1)
path2 = basePath.split('\\\\')[:-1] + ['transfer'] + ['gif_triggers.db']
path2 = '\\\\'.join(path2)

# ========== CONNECTION 1 ===========
connection = sql.connect(path1)
cursor = connection.cursor()
print('connected: ' + path1)

cursor.execute(""" SELECT * FROM userstats """)
data = cursor.fetchall()

UserService.clear_table()
for row in data:
    newUser = User(userId=row[0], exp=row[1], level=row[2], messagesCount=row[3],
                   symbolsCount=row[4], voiceChatTime=row[5])
    newUser.voluteCount = 0
    newUser.expModifier = 0
    UserService.add_new_user(userId=newUser.userId)
    UserService.update_user(user=newUser)

print('data copied')
connection.close()
print('connection closed')

# ========== CONNECTION 2 ===========
GifService.clear_table()
GifGroupService.clear_table()

connection = sql.connect(path2)
cursor = connection.cursor()
print('connected: ' + path2)

# ========== table 1 ===========
cursor.execute(""" SELECT * FROM triggers """)
data = cursor.fetchall()
idDict = {}
i = 1
for row in data:
    newGifGroup = GifGroup(name=row[0], authorId=row[1], phrase=row[2], accessLevel=row[3],
                           createDate=datetime.strftime(datetime.now(), "%Y-%m-%d"))
    GifGroupService.add_new_gif_group_full(gifGroup=newGifGroup)
    idDict[row[0]] = i
    i += 1

# ========== table 2 ===========
cursor.execute(""" SELECT * FROM gif """)
data = cursor.fetchall()

for row in data:
    newGif = Gif(groupId=idDict[row[0]], gifUrl=row[1])
    GifService.add_new_gif(gif=newGif)

print('data copied')
connection.close()
print('connection closed')
