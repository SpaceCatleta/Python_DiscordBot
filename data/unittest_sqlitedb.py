import unittest
from data import sqlitedb
from structs import userstats


# Тестирует класс data.sqlitedb.BotDataBase
class Test_BotDataBase(unittest.TestCase):
    DB: sqlitedb.BotDataBase

    @classmethod
    def setUpClass(cls):
        cls.DB = sqlitedb.BotDataBase('TestDB.db')
        cls.DB.cursor.execute("""
        SELECT * FROM sqlite_master
        WHERE type = 'table'
        """)
        print(cls.DB.cursor.fetchall())

    @classmethod
    def tearDownClass(cls):
        cls.DB.close()

    def setUp(self):
        self.DB.cursor.execute("INSERT INTO userstats VALUES ({0}, {1}, {2}, {3}, {4}, {5}, '{6}');".format(123,
            10, 1, 2, 100, 600, 'user001'))
        self.DB.connect.commit()

    def tearDown(self):
        self.DB.cursor.execute('DELETE FROM userstats;')
        self.DB.connect.commit()

    def test_select(self):
        print('Testing sqlitedb.BotDataBase.select()')
        stat: userstats.userstats = self.DB.select(123)
        self.assertEqual(10, stat.exp, 'exp mismatch')
        self.assertEqual(1, stat.lvl, 'lvl mismatch')
        self.assertEqual(2, stat.mes_counter, 'mes_counter mismatch')
        self.assertEqual(100, stat.symb_counter, 'symb_counter mismatch')
        self.assertEqual(600, stat.vc_counter, 'vc_counter mismatch')
        self.assertEqual('user001', stat.name, 'name mismatch')

    def test_insert(self):
        print('Testing sqlitedb.BotDataBase.insert()')
        stat: userstats.userstats = userstats.userstats(ID=1,  Exp=int(5), Lvl=int(0),
            MesCounter=int(10), SymbCounter=int(100),
            VCCounter=int(1000), Name='user002')
        self.DB.insert(stat=stat)
        stat = self.DB.select(1)
        self.assertEqual(1, stat.id, 'id mismatch')
        self.assertEqual(5, stat.exp, 'exp mismatch')
        self.assertEqual(0, stat.lvl, 'lvl mismatch')
        self.assertEqual(10, stat.mes_counter, 'mes_counter mismatch')
        self.assertEqual(100, stat.symb_counter, 'symb_counter mismatch')
        self.assertEqual(1000, stat.vc_counter, 'vc_counter mismatch')
        self.assertEqual('user002', stat.name, 'name mismatch')

    def test_update(self):
        print('Testing sqlitedb.BotDataBase.update()')
        stat: userstats.userstats = userstats.userstats(ID=123, Exp=int(10), Lvl=int(10),
                                                        MesCounter=int(10), SymbCounter=int(10),
                                                        VCCounter=int(10), Name='user0001')
        self.DB.update(stat=stat)
        stat = self.DB.select(123)
        self.assertEqual(123, stat.id, 'id mismatch')
        self.assertEqual(10, stat.exp, 'exp mismatch')
        self.assertEqual(10, stat.lvl, 'lvl mismatch')
        self.assertEqual(10, stat.mes_counter, 'mes_counter mismatch')
        self.assertEqual(10, stat.symb_counter, 'symb_counter mismatch')
        self.assertEqual(10, stat.vc_counter, 'vc_counter mismatch')
        self.assertEqual('user0001', stat.name, 'name mismatch')

    def test_update_with_addition(self):
        print('Testing sqlitedb.BotDataBase.update_with_addition()')
        stat: userstats.userstats = userstats.userstats(ID=123, Exp=int(100), MesCounter=int(1), Name='noname001')
        self.DB.update_with_addition(stat=stat)
        stat = self.DB.select(123)
        self.assertEqual(123, stat.id, 'id mismatch')
        self.assertEqual(110, stat.exp, 'exp mismatch')
        self.assertEqual(1, stat.lvl, 'lvl mismatch')
        self.assertEqual(3, stat.mes_counter, 'mes_counter mismatch')
        self.assertEqual(100, stat.symb_counter, 'symb_counter mismatch')
        self.assertEqual(600, stat.vc_counter, 'vc_counter mismatch')
        self.assertEqual('noname001', stat.name, 'name mismatch')


# Тестирует класс data.sqlitedb.BotDataBase
class Test_BotDataBase_SettingsTable(unittest.TestCase):
    DB: sqlitedb.BotDataBase

    @classmethod
    def setUpClass(cls):
        cls.DB = sqlitedb.BotDataBase('TestDB.db')

    @classmethod
    def tearDownClass(cls):
        cls.DB.close()

    def setUp(self):
        self.DB.cursor.execute("INSERT INTO settings VALUES ('name1', 'setting1');")
        self.DB.connect.commit()

    def tearDown(self):
        self.DB.cursor.execute('DELETE FROM settings;')
        self.DB.connect.commit()

    def test_select_settings(self):
        print('Testing sqlitedb.BotDataBase.select_settings()')
        settings = self.DB.select_settings()
        self.assertEqual('setting1', settings['name1'], 'setting mismatch')

    def test_update_setting(self):
        print('Testing sqlitedb.BotDataBase.update_setting()')
        self.DB.update_setting('name1', 'newsetting')
        settings = self.DB.select_settings()
        self.assertEqual('newsetting', settings['name1'], 'setting mismatch')


if __name__ == '__main__':
    unittest.main()
