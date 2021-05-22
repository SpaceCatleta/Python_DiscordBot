import sqlite3 as sql


class Gif_Trigger:
    author_id: int
    name: str
    discr: str = 'None'
    access: bool = False
    gif_list = []
    count: int = 0

    def __init__(self, author_id: int, name: str, discr: str='None'):
        self.name = name
        self.author_id = author_id
        self.discr = discr
        self.access = False
        self.gif_list = []


class GifTriggersDataBase:
    connect: sql.Connection
    cursor: sql.Cursor

    def __init__(self, path: str):
        self.connect = sql.connect(path)
        self.cursor = self.connect.cursor()

    def close(self):
        self.connect.close()

    def add_new_trigger(self, item: Gif_Trigger):
        self.cursor.execute("insert into triggers values ('{0}', {1}, '{2}', {3});".
                            format(item.name, item.author_id, item.discr, item.access))
        self.connect.commit()

    def get_trigger(self, name: str):
        self.cursor.execute("""
        SELECT * from triggers
        WHERE name='{0}'
        """.format(name))
        row: sql.Row = self.cursor.fetchone()
        if row is None:
            return None
        else:
            trigger = Gif_Trigger(name=name, author_id=int(row[1]), discr=row[2])
            trigger.access = False if int(row[3]) == 0 else True
            return trigger

    def add_gif(self, group_name: str, url: str):
        print(url)
        self.cursor.execute("insert into gif values ('{0}', '{1}');".format(group_name, url))
        self.connect.commit()

    def get_triggers_list(self):
        self.cursor.execute("""
                SELECT group_name, Count(group_name)
                FROM gif
                GROUP BY group_name""")
        records = self.cursor.fetchall()

        self.cursor.execute("""
                SELECT *
                FROM triggers""")
        records2 = self.cursor.fetchall()

        triggers = []
        for row in records2:
            item = Gif_Trigger(name=row[0],author_id=row[1], discr=row[2])
            item.access = row[3]

            for rec in records:
                if rec[0] == item.name:
                    item.count = rec[1]
                    records.remove(rec)

            triggers.append(item)

        return triggers

    def get_group_gif(self, name: str):
        self.cursor.execute("""
        SELECT gif from gif
        WHERE group_name='{0}'
        """.format(name))

        records = self.cursor.fetchall()
        return records

    def switch_lock(self, name):
        trigger = self.get_trigger(name=name)
        if trigger is None:
            return -1
        new_val: int = 1 if trigger.access == 0 else 1
        self.cursor.execute("""UPDATE triggers
        SET access={0} 
        WHERE name='{1}'""".format(new_val, trigger.name))
        self.connect.commit()
        return 0

    def update_trigger_discr(self, name: str, new_discr: str):
        trigger = self.get_trigger(name=name)
        if trigger is None:
            return -1
        self.cursor.execute("""UPDATE triggers
                SET discr='{0}' 
                WHERE name='{1}'""".format(new_discr, trigger.name))
        self.connect.commit()
        return 0

    def delete_trigger(self, name):
        ans = self.get_trigger(name=name)
        if ans is None:
            return -1
        self.cursor.execute("""DELETE FROM triggers
                WHERE name='{0}'""".format(ans.name))
        self.cursor.execute("""DELETE FROM gif
                        WHERE group_name='{0}'""".format(ans.name))
        self.connect.commit()
        return 0


    def delete_gif(self, group_name: str, url: str):
        self.cursor.execute("""DELETE FROM gif
                WHERE group_name='{0}'
                AND gif='{1}'""".format(group_name, url))
        self.connect.commit()
