import sqlite3 as sql
from structs import userstats


class BotDataBase:
    connect: sql.Connection
    cursor: sql.Cursor

    def __init__(self, path: str):
        self.connect = sql.connect(path)
        self.cursor = self.connect.cursor()

    def close(self):
        self.connect.close()

    def create_1(self):
        self.cursor.execute("""
        CREATE TABLE "userstats" (
        "id"	INTEGER,
        "exp"	REAL,
        "level"	INTEGER,
        "messages_sent"	INTEGER,
        "symbols_print"	INTEGER,
        "vc_time"	INTEGER,
        "username"	INTEGER,
        PRIMARY KEY("id"));
        """)

    def select(self, id: int):
        self.cursor.execute("""
        SELECT * from userstats
        WHERE id={0}
        """.format(id))
        row: sql.Row = self.cursor.fetchone()
        return userstats.userstats(ID=id,  Exp=int(row[1]), Lvl=int(row[2]),
            MesCounter=int(row[3]), SymbCounter=int(row[4]),
            VCCounter=int(row[5]), Name=row[6])

    def insert(self, stat: userstats.userstats):
        self.cursor.execute("insert into userstats values ({0}, {1}, {2}, {3}, {4}, {5}, '{6}');".format(stat.id,
            stat.exp, stat.lvl, stat.mes_counter, stat.symb_counter, stat.vc_counter, stat.name))
        self.connect.commit()

    def insert_list(self, statlist):
        for stat in statlist:
            self.insert(stat)

    def update(self, stat: userstats.userstats):
        self.cursor.execute("""
          UPDATE userstats
          SET exp={1}, level={2}, messages_sent={3}, symbols_print={4}, vc_time={5}, username='{6}'  
          WHERE id={0}
        """.format(stat.id, stat.exp, stat.lvl, stat.mes_counter, stat.symb_counter, stat.vc_counter, stat.name))
        self.connect.commit()

    def update_with_addition(self, stat: userstats.userstats):
        stat2: userstats.userstats = self.select(stat.id)
        stat.add(stat2)
        self.update(stat)

    def select_settings(self):
        self.cursor.execute("SELECT *  FROM settings")
        settinglist = self.cursor.fetchall()
        settingdict = {}
        for row in settinglist:
            settingdict[row[0]] = row[1]
        return settingdict

    def update_setting(self, name: str, setting: str):
            self.cursor.execute("""
            UPDATE settings
            SET setting='{0}'
            WHERE name='{1}'
            """.format(setting, name))
            self.connect.commit()
