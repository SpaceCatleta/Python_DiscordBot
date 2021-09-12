import botdb.database


path = str(botdb)
path = path.split("'")[-2]
path = path.split('\\\\')[:-1] + ['BotDB.db']
path = '\\\\'.join(path)

database.open(path=path)