import unittest
from botdb.services import UserService
from botdb.entities.User import User


class TestUserService(unittest.TestCase):

    def _check_data(self, checking_obj: User, control_obj: User):
        for field in checking_obj.__dict__.keys():
            value = checking_obj.__dict__[field]
            controlValue = control_obj.__dict__[field]
            self.assertEqual(value, controlValue, '{2} should be {0} actual {1}'.format(controlValue, value, field))

    def setUp(self):
        UserService.clear_table()
        UserService.add_new_user(userId=11)
        UserService.add_new_user(userId=12)

    @classmethod
    def tearDownClass(cls):
        UserService.clear_table()

    def test_add_new_user_and_get_user_by_id(self):
        print('Testing add_new_user() and get_user_bu_id()')
        checkUser = User(userId=100000000000000000, exp=0.0, level=0, messagesCount=0,
                         symbolsCount=0, voiceChatTime=0, voluteCount=0, expModifier=0)

        UserService.add_new_user(userId=100000000000000000)
        user = UserService.get_user_by_id(userId=100000000000000000)

        self._check_data(checking_obj=user, control_obj=checkUser)
        print('Successful\n')
    # =====================

    # =====================
    def test_get_all_users(self):
        print('Testing get_all_users()')
        checkUser = User(userId=11, exp=0.0, level=0, messagesCount=0,
                         symbolsCount=0, voiceChatTime=0, voluteCount=0, expModifier=0)

        userList = UserService.get_all_users()

        self.assertEqual(2, len(userList), 'exp should be {0} actual {1}'.format(2, len(userList)))
        self._check_data(checking_obj=userList[0], control_obj=checkUser)
        print('Successful\n')
    # =====================

    # =====================
    def test_get_top10_by_exp(self):
        print('Testing get_top10_by_exp()')
        user1 = User(userId=13, exp=10, level=0, messagesCount=0,
                     symbolsCount=0, voiceChatTime=0, voluteCount=0, expModifier=0)
        UserService.add_new_user(userId=13)
        UserService.update_user(user=user1)
        user2 = User(userId=14, exp=1000, level=0, messagesCount=0,
                     symbolsCount=0, voiceChatTime=0, voluteCount=0, expModifier=0)
        UserService.add_new_user(userId=14)
        UserService.update_user(user=user2)
        user3 = User(userId=15, exp=300, level=0, messagesCount=0,
                     symbolsCount=0, voiceChatTime=0, voluteCount=0, expModifier=0)
        UserService.add_new_user(userId=15)
        UserService.update_user(user=user3)

        userList = UserService.get_top10_by_exp()

        self.assertEqual(14, userList[0].userId, 'userId should be {0} actual {1}'.format(14, userList[0].userId))
        print('Successful\n')
    # =====================

    # =====================
    def test_update_user(self):
        print('Testing update_user()')
        user = User(userId=11, exp=1230, level=3, messagesCount=100, symbolsCount=1000,
                    voiceChatTime=3600, voluteCount=500, expModifier=-100)

        UserService.update_user(user=user)
        ansUser = UserService.get_user_by_id(userId=11)

        self._check_data(checking_obj=ansUser, control_obj=user)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_stats_on_messages(self):
        print('Testing update_stats_on_messages()')
        user = User(userId=11, exp=310, level=0, messagesCount=10, symbolsCount=300,
                    voiceChatTime=0, voluteCount=0, expModifier=0)
        checkUser = User(userId=11, exp=620, level=0, messagesCount=20, symbolsCount=600,
                         voiceChatTime=0, voluteCount=0, expModifier=0)

        UserService.append_stats_on_messages(user=user)
        UserService.append_stats_on_messages(user=user)
        user = UserService.get_user_by_id(userId=11)

        self._check_data(checking_obj=user, control_obj=checkUser)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_stats_on_voice_chat(self):
        print('Testing update_stats_on_voice_chat()')
        user = User(userId=11, exp=12, level=0, messagesCount=0, symbolsCount=0,
                    voiceChatTime=600, voluteCount=0, expModifier=0)
        checkUser = User(userId=11, exp=24, level=0, messagesCount=0, symbolsCount=0,
                         voiceChatTime=1200, voluteCount=0, expModifier=0)

        UserService.append_stats_on_voice_chat(user=user)
        UserService.append_stats_on_voice_chat(user=user)
        user = UserService.get_user_by_id(userId=11)

        self._check_data(checking_obj=user, control_obj=checkUser)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_user_level(self):
        print('Testing update_user_level()')
        user = User(userId=11, exp=0, level=4, messagesCount=0, symbolsCount=0,
                    voiceChatTime=0, voluteCount=0, expModifier=0)

        UserService.update_user_level(user=user)
        user2 = UserService.get_user_by_id(userId=11)

        self._check_data(checking_obj=user2, control_obj=user)
        print('Successful\n')
    # =====================

    # =====================
    def test_add_user_exp_modifier(self):
        print('Testing add_user_expModifier()')
        user = User(userId=11, exp=200, level=0, messagesCount=0, symbolsCount=0,
                    voiceChatTime=0, voluteCount=0, expModifier=200)
        checkUser = User(userId=11, exp=400, level=0, messagesCount=0, symbolsCount=0,
                         voiceChatTime=0, voluteCount=0, expModifier=400)

        UserService.add_user_exp_modifier(user=user)
        UserService.add_user_exp_modifier(user=user)
        user = UserService.get_user_by_id(userId=11)

        self._check_data(checking_obj=user, control_obj=checkUser)
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_user_by_id(self):
        print('Testing delete_user_by_id()')

        UserService.delete_user_by_id(11)
        userList = UserService.get_all_users()

        self.assertEqual(1, len(userList), 'exp should be {0} actual {1}'.format(1, len(userList)))
        print('Successful\n')
    # =====================


if __name__ == '__main__':
    print('boot unit tests')
    unittest.main()
