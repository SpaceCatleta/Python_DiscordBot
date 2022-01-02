import unittest
from datetime import datetime as DateTime
from botdb.services import GuildService
from botdb.services import UserService
from botdb.services import GuildUserService
from botdb.entities.GuildUser import GuildMember


class TestGuildMemberService(unittest.TestCase):

    def _check_data(self, checking_obj: GuildMember, control_obj: GuildMember):
        for field in checking_obj.__dict__.keys():
            value = checking_obj.__dict__[field]
            controlValue = control_obj.__dict__[field]
            self.assertEqual(value, controlValue, '{2} should be {0} actual {1}'.format(controlValue, value, field))

    @classmethod
    def setUpClass(cls):
        GuildUserService.clear_table()
        UserService.clear_table()
        GuildService.clear_table()

        GuildService.add_new_guild(guildId=101)
        GuildService.add_new_guild(guildId=102)
        GuildService.add_new_guild(guildId=103)

        UserService.add_new_user(userId=11)
        UserService.add_new_user(userId=12)
        UserService.add_new_user(userId=13)

        print('\n[[[   TESTING GuildMemberService   ]]]\n')

    def setUp(self):
        GuildUserService.clear_table()

        GuildUserService.add_guild_member(guildMember=GuildMember(guildId=101, userId=11))
        GuildUserService.add_guild_member(guildMember=GuildMember(guildId=101, userId=12))
        GuildUserService.add_guild_member(guildMember=GuildMember(guildId=102, userId=13))

    @classmethod
    def tearDownClass(cls):
        GuildUserService.clear_table()
        UserService.clear_table()
        GuildService.clear_table()
    # =====================

    # =====================
    def test_add_guild_member_and_get_guild_member_by_ids(self):
        print('Testing add_guild_member() and get_guild_member_by_ids()')
        member = GuildMember(guildId=103, userId=11, visitsCount=1, warningsCount=0, banBotFunctions=0)

        GuildUserService.add_guild_member(guildMember=member)

        answer = GuildUserService.get_guild_member_by_ids(guildId=member.guildId, userId=member.userId)
        self._check_data(checking_obj=answer, control_obj=member)
        print('Successful\n')
    # =====================

    # =====================
    def test_get_all_guild_members(self):
        print('Testing get_all_guild_members()')

        answer = len(GuildUserService.get_all_guild_members())
        self.assertEqual(answer, 3, 'rows_count should be {0} actual {1}'.format(3, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_get_members_count(self):
        print('Testing get_members_count()')

        answer = GuildUserService.get_members_count()
        self.assertEqual(answer, 3, 'rows_count should be {0} actual {1}'.format(3, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_get_members_count_by_guild_id(self):
        print('Testing get_members_count_by_guild_id()')

        answer = GuildUserService.get_members_count_by_guild_id(guildId=101)
        self.assertEqual(answer, 2, 'rows_count should be {0} actual {1}'.format(2, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_update_guild_member(self):
        print('Testing update_guild_member()')
        member = GuildMember(guildId=102, userId=13, visitsCount=2, warningsCount=2,
                             banBotFunctions=1, personalRoleId=123, punishmentRoleId=123,
                             punishmentEndDate=DateTime.strptime('2021-10-10 12:30:12', "%Y-%m-%d %H:%M:%S"))
        GuildUserService.update_guild_member(guildMember=member)
        member2 = GuildUserService.get_guild_member_by_ids(guildId=102, userId=13)
        self._check_data(checking_obj=member2, control_obj=member)
        print('Successful\n')
    # =====================

    def test_update_guild_member_personal_role(self):
        print('Testing update_guild_member_personal_role()')
        member = GuildMember(guildId=102, userId=13, visitsCount=1, warningsCount=0,
                             banBotFunctions=0, personalRoleId=123)
        GuildUserService.update_guild_member_personal_role(guildMember=member)
        member2 = GuildUserService.get_guild_member_by_ids(guildId=102, userId=13)
        self._check_data(checking_obj=member2, control_obj=member)
        print('Successful\n')
    # =====================

    def test_update_guild_member_ban_func(self):
        print('Testing update_guild_member_ban_func()')
        member = GuildMember(guildId=102, userId=13, visitsCount=1, warningsCount=0, banBotFunctions=1)
        GuildUserService.update_guild_member_ban_func(guildMember=member)
        member2 = GuildUserService.get_guild_member_by_ids(guildId=102, userId=13)
        self._check_data(checking_obj=member2, control_obj=member)
        print('Successful\n')
    # =====================

    # =====================
    def update_guild_member_punishment(self):
        print('Testing update_guild_member_punishment()')
        member = GuildMember(guildId=102, userId=13, visitsCount=1, warningsCount=0,
                             banBotFunctions=0, punishmentRoleId=123,
                             punishmentEndDate=DateTime.strptime('2021-10-10 12:30:12', "%Y-%m-%d %H:%M:%S"))
        GuildUserService.update_guild_member_punishment(guildMember=member)
        member2 = GuildUserService.get_guild_member_by_ids(guildId=102, userId=13)
        self._check_data(checking_obj=member2, control_obj=member)
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_guild_member_by_ids(self):
        print('Testing delete_guild_member_by_ids()')
        GuildUserService.delete_guild_member_by_ids(guildId=101, userId=11)

        answer = GuildUserService.get_members_count_by_guild_id(guildId=101)
        self.assertEqual(answer, 1, 'rows_count should be {0} actual {1}'.format(1, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_guild_members_guild_id(self):
        print('Testing delete_guild_members_guild_id()')
        GuildUserService.delete_guild_members_guild_id(guildId=101)

        answer = GuildUserService.get_members_count_by_guild_id(guildId=101)
        self.assertEqual(answer, 0, 'rows_count should be {0} actual {1}'.format(0, answer))
        print('Successful\n')
    # =====================


if __name__ == '__main__':
    print('boot unit tests')
    unittest.main()
