import unittest
from botdb.services import GuildService
from botdb.services import LevelRoleService
from botdb.entities.LevelRole import LevelRole


class TestLevelRoleService(unittest.TestCase):

    def _check_data(self, checking_obj: LevelRole, control_obj: LevelRole):
        for field in checking_obj.__dict__.keys():
            value = checking_obj.__dict__[field]
            controlValue = control_obj.__dict__[field]
            self.assertEqual(value, controlValue, '{2} should be {0} actual {1}'.format(controlValue, value, field))

    @classmethod
    def setUpClass(cls):
        LevelRoleService.clear_table()
        GuildService.clear_table()
        GuildService.add_new_guild(guildId=1234)
        GuildService.add_new_guild(guildId=4444)
        print('\n[[[   TESTING GifGroupService   ]]]\n')

    def setUp(self):
        LevelRoleService.clear_table()
        LevelRoleService.add_level_role(LevelRole(guildId=1234, level=1, roleId=123))
        LevelRoleService.add_level_role(LevelRole(guildId=1234, level=5, roleId=1234))
        LevelRoleService.add_level_role(LevelRole(guildId=4444, level=10, roleId=12345))

    @classmethod
    def tearDownClass(cls):
        LevelRoleService.clear_table()
        GuildService.clear_table()

    # =====================
    def test_add_and_get_all(self):
        print('Testing add_level_role() and get_all_level_roles()')
        LevelRoleService.add_level_role(LevelRole(guildId=1234, level=29, roleId=100))

        roleList = LevelRoleService.get_all_level_roles()
        checkList = [LevelRole(guildId=1234, level=1, roleId=123), LevelRole(guildId=1234, level=5, roleId=1234),
                     LevelRole(guildId=4444, level=10, roleId=12345), LevelRole(guildId=1234, level=29, roleId=100)]

        for i in range(len(roleList)):
            self._check_data(checking_obj=roleList[i], control_obj=checkList[i])
        print('Successful\n')
    # =====================

    # =====================
    def test_get_level_roles_dict_by_guild_id(self):
        print('Testing get_level_roles_dict_by_guild_id()')

        roleDict = LevelRoleService.get_level_roles_dict_by_guild_id(guildId=1234)
        checkDict = {1: LevelRole(guildId=1234, level=1, roleId=123), 5: LevelRole(guildId=1234, level=5, roleId=1234)}

        self._check_data(checking_obj=roleDict[1], control_obj=checkDict[1])
        self._check_data(checking_obj=roleDict[5], control_obj=checkDict[5])
        print('Successful\n')
    # =====================

    # =====================
    def test_get_all_level_roles_count(self):
        print('Testing get_all_level_roles_count()')

        answer = LevelRoleService.get_all_level_roles_count()

        self.assertEqual(3, answer, 'rows_count should be {0} actual {1}'.format(3, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_get_level_roles_count_by_guild_id(self):
        print('Testing get_level_roles_count_by_guild_id()')

        answer = LevelRoleService.get_level_roles_count_by_guild_id(guildId=1234)

        self.assertEqual(2, answer, 'rows_count should be {0} actual {1}'.format(2, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_update_level_role(self):
        print('Testing update_level_role()')
        newRole = LevelRole(guildId=4444, level=10, roleId=111)
        LevelRoleService.update_level_role(levelRole=newRole)

        rolesDict = LevelRoleService.get_level_roles_dict_by_guild_id(guildId=4444)

        self._check_data(checking_obj=rolesDict[10], control_obj=newRole)
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_level_role(self):
        print('Testing delete_level_role()')
        newRole = LevelRole(guildId=1234, level=1, roleId=123)
        LevelRoleService.delete_level_role(levelRole=newRole)

        answer = LevelRoleService.get_level_roles_count_by_guild_id(guildId=1234)

        self.assertEqual(1, answer, 'rows_count should be {0} actual {1}'.format(1, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_level_roles_by_guild_id(self):
        print('Testing delete_level_roles_by_guild_id()')
        LevelRoleService.delete_level_roles_by_guild_id(guildId=1234)

        answer = LevelRoleService.get_level_roles_count_by_guild_id(guildId=1234)

        self.assertEqual(0, answer, 'rows_count should be {0} actual {1}'.format(0, answer))
        print('Successful\n')
    # =====================


if __name__ == '__main__':
    print('boot unit tests')
    unittest.main()
