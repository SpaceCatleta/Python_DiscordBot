import unittest
from botdb.services import GuildService
from botdb.services import LevelRoleService
from botdb.entities.Guild import Guild
from botdb.entities.LevelRole import LevelRole


class TestUserVoiceChatService(unittest.TestCase):

    def _check_guild_data(self, checking_obj: Guild, control_obj: Guild):
        for field in checking_obj.__dict__.keys():
            value = checking_obj.__dict__[field]
            controlValue = control_obj.__dict__[field]
            self.assertEqual(value, controlValue, '{2} should be {0} actual {1}'.format(controlValue, value, field))

    def setUp(self):
        LevelRoleService.clear_table()
        GuildService.clear_table()
        GuildService.add_new_guild(guildId=1234)
        GuildService.add_new_guild(guildId=4444)

    @classmethod
    def tearDownClass(cls):
        LevelRoleService.clear_table()
        GuildService.clear_table()
    # =====================

    # =====================
    def test_add_new_guild_and_get_guild_by_guild_id(self):
        print('Testing add_new_guild() and get_guild_by_guild_id()')
        GuildService.add_new_guild(guildId=1122)
        guild = GuildService.get_guild_by_guild_id(guildId=1122)
        self._check_guild_data(checking_obj=guild,
                               control_obj=Guild(guildId=1122, maxLinks=10, muteTime=10, personalRolesAllowed=0))
        print('Successful\n')
    # =====================

    # =====================
    def test_get_all_guilds(self):
        print('Testing get_all_guilds()')

        answer = GuildService.get_all_guilds()

        self.assertEqual(2, len(answer), 'rows_count should be {0} actual {1}'.format(2, len(answer)))
        print('Successful\n')
    # =====================

    # =====================
    def test_get_guilds_count(self):
        print('Testing get_guilds_count()')

        answer = GuildService.get_guilds_count()

        self.assertEqual(2, answer, 'rows_count should be {0} actual {1}'.format(2, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_get_guild_boot_setup(self):
        print('Testing get_guild_boot_setup()')
        LevelRoleService.add_level_role(levelRole=LevelRole(guildId=1234, level=1, roleId=10))
        LevelRoleService.add_level_role(levelRole=LevelRole(guildId=1234, level=5, roleId=20))
        LevelRoleService.add_level_role(levelRole=LevelRole(guildId=1234, level=9, roleId=30))
        LevelRoleService.add_level_role(levelRole=LevelRole(guildId=4444, level=1, roleId=40))
        LevelRoleService.add_level_role(levelRole=LevelRole(guildId=4444, level=5, roleId=50))

        guildDict = GuildService.get_guild_boot_setup()

        self.assertEqual(3, len(guildDict[1234].levelsMap), 'rows_count should be {0} actual {1}'.
                         format(3, len(guildDict[1234].levelsMap)))
        self.assertEqual(2, len(guildDict[4444].levelsMap), 'rows_count should be {0} actual {1}'.
                         format(2, len(guildDict[4444].levelsMap)))
        print('Successful\n')
    # =====================

    # =====================
    def test_update_guild_full(self):
        print('Testing update_guild_full()')
        guild = GuildService.get_guild_by_guild_id(guildId=1234)
        guild.CHIELDChatId = 12345
        guild.welcomePhrase = 'hi there'
        guild.personalRolesAllowed = 1
        guild.membersCounterChatId = 4321
        guild.noLinksRoleId = 1000
        GuildService.update_guild_full(guild=guild)

        guild2 = GuildService.get_guild_by_guild_id(guildId=1234)

        self._check_guild_data(checking_obj=guild2, control_obj=guild)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_guild_common(self):
        print('Testing update_guild_common()')
        guild = GuildService.get_guild_by_guild_id(guildId=1234)
        guild.maxLinks = 15
        guild.muteTime = 60
        guild.personalRolesAllowed = 1
        GuildService.update_guild_common(guild=guild)

        guild2 = GuildService.get_guild_by_guild_id(guildId=1234)

        self._check_guild_data(checking_obj=guild2, control_obj=guild)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_guild_roles(self):
        print('Testing update_guild_roles()')
        guild = GuildService.get_guild_by_guild_id(guildId=1234)
        guild.banBotFunctions = 11234
        guild.noLinksRoleId = 11235
        guild.lightMuteRoleId = 11236
        guild.muteRoleId = 11237
        guild.muteVoiceChatRoleId = 11238
        GuildService.update_guild_roles(guild=guild)

        guild2 = GuildService.get_guild_by_guild_id(guildId=1234)

        self._check_guild_data(checking_obj=guild2, control_obj=guild)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_guild_shield_settings(self):
        print('Testing update_guild_shield_settings()')
        guild = GuildService.get_guild_by_guild_id(guildId=1234)
        guild.CHIELDChatId = 1234
        guild.CHIELDWarningCount = 5
        guild.CHIELDAlertCount = 20
        GuildService.update_guild_shield_settings(guild=guild)

        guild2 = GuildService.get_guild_by_guild_id(guildId=1234)

        self._check_guild_data(checking_obj=guild2, control_obj=guild)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_guild_chats(self):
        print('Testing update_guild_shield_settings()')
        guild = GuildService.get_guild_by_guild_id(guildId=1234)
        guild.voiceChatCreatorId = 1432
        guild.membersCounterChatId = 3241
        guild.rolesCounterChatId = 6521
        GuildService.update_guild_chats(guild=guild)

        guild2 = GuildService.get_guild_by_guild_id(guildId=1234)

        self._check_guild_data(checking_obj=guild2, control_obj=guild)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_guild_welcome_phrase(self):
        print('Testing update_guild_welcome_phrase()')
        guild = GuildService.get_guild_by_guild_id(guildId=1234)
        guild.welcomePhrase = 'приветсвуем'
        GuildService.update_guild_welcome_phrase(guild=guild)

        guild2 = GuildService.get_guild_by_guild_id(guildId=1234)

        self._check_guild_data(checking_obj=guild2, control_obj=guild)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_welcome_gif_group_id(self):
        print('Testing update_welcome_gif_group_id()')
        guild = GuildService.get_guild_by_guild_id(guildId=1234)
        guild.welcomeGifGroupId = 1
        GuildService.update_welcome_gif_group_id(guild=guild)

        guild2 = GuildService.get_guild_by_guild_id(guildId=1234)

        self._check_guild_data(checking_obj=guild2, control_obj=guild)
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_guild_by_guild_id(self):
        print('Testing delete_guild_by_guild_id()')
        GuildService.delete_guild_by_guild_id(guildId=4444)

        answer = GuildService.get_guilds_count()

        self.assertEqual(1, answer, 'rows_count should be {0} actual {1}'.format(1, answer))
        print('Successful\n')


if __name__ == '__main__':
    print('boot unit tests')
    unittest.main()
