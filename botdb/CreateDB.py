import database

database.open('BotDB.db')

with open('CreationScript.sql') as SQLFile:
    sqlText = SQLFile.read()

tableTexts = sqlText.split('=====\n')
for text in tableTexts:
    database.cursor.execute(text)
    database.connection.commit()
    print(text.split('\n')[1])
print('tables created')
database.close()
