import unittest
import structs.userstats as struct
import structs.userstatslist as usList


# Тестирует класс structs.userstats
class Test_UserStats(unittest.TestCase):
    us1: struct.userstats
    us2: struct.userstats

    def setUp(self):
        self.us1 = struct.userstats(ID=1, SymbCounter=10,
                                    MesCounter=1, VCCounter=10, Exp=2, Lvl=1, Name='us1')
        self.us2 = struct.userstats(ID=2, SymbCounter=20,
                                    MesCounter=2, VCCounter=20, Exp=4, Lvl=2, Name='us2')


    def test_userstats_add(self):
        print('Testing structs.userstats.add()')
        self.us1.add(self.us2)
        self.assertEqual(6, self.us1.exp, 'exp should be 6 actual ' + str(self.us1.exp))
        self.assertEqual(3, self.us1.lvl, 'lvl should be 3 actual ' + str(self.us1.lvl))
        self.assertEqual(3, self.us1.mes_counter, 'mes_counter should be 3 actual ' + str(self.us1.mes_counter))
        self.assertEqual(30, self.us1.symb_counter, 'symb_counter should be 30 actual ' + str(self.us1.symb_counter))
        self.assertEqual(30, self.us1.vc_counter, 'vc_counter should be 30 actual ' + str(self.us1.vc_counter))

    def test_userstats_clear(self):
        print('Testing structs.userstats.clear()')
        self.us1.clear()
        self.assertEqual(0, self.us1.exp, 'exp should be 0 actual ' + str(self.us1.exp))
        self.assertEqual(0, self.us1.lvl, 'lvl should be 0 actual ' + str(self.us1.lvl))
        self.assertEqual(0, self.us1.mes_counter, 'mes_counter should be 0 actual ' + str(self.us1.mes_counter))
        self.assertEqual(0, self.us1.symb_counter, 'symb_counter should be 0 actual ' + str(self.us1.symb_counter))
        self.assertEqual(10, self.us1.vc_counter,
                         'vc_counter should be 10 [clear(vc_clear=False)] actual ' + str(self.us1.vc_counter))
        self.us1.clear(vc_clear=True)
        self.assertEqual(0, self.us1.vc_counter,
                         'vc_counter should be 0 [clear(vc_clear=True)] actual ' + str(self.us1.vc_counter))


# Тестирует класс structs.UsersstatsList
class Test_UsersStatsList(unittest.TestCase):
    usl1: usList.UserStatsList
    usl2: usList.UserStatsList

    def setUp(self):
        self.usl1 = usList.UserStatsList()
        self.usl1.push(struct.userstats(ID=1, Exp=10))
        self.usl1.push(struct.userstats(ID=2, Exp=20))
        self.usl2 = usList.UserStatsList()
        self.usl2.push(struct.userstats(ID=2, Exp=30))
        self.usl2.push(struct.userstats(ID=3, Exp=40))

    def test_userstatslist_search_id(self):
        print('Testing structs.userstatslist.search_id()')
        us: struct.userstats = self.usl1.search_id(1)
        self.assertEqual(1, us.id, 'mismatch')
        us =  self.usl1.search_id(10)
        self.assertEqual(None, us, 'mismatch')

    def test_userstatslist_merge_with(self):
        print('Testing structs.userstatslist.merge_with()')
        self.usl1.merge_with(self.usl2)
        self.assertEqual(3, self.usl1.count, 'count mismatch')
        self.assertEqual(10, self.usl1.search_id(1).exp, 'mismatch 1')
        self.assertEqual(50, self.usl1.search_id(2).exp, 'mismatch 2')
        self.assertEqual(40, self.usl1.search_id(3).exp, 'mismatch 3')


if __name__ == '__main__':
    unittest.main()
