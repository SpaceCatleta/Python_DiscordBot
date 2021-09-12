import database

database.open('BotDB.db')

with open('CreationScript.sql') as SQLFile:
    sqlText = SQLFile.read()

tableTexts = sqlText.split('=====')
for text in tableTexts:
    database.cursor.execute(text)
    database.connection.commit()
print('tables created')
database.close()
