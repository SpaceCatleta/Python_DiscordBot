import unittest
from botdb.services import UserService
from botdb.services import UserVoiceChatService
from botdb.entities.UserVoiceChat import UserVoiceChat


class TestUserVoiceChatService(unittest.TestCase):

    def _check_data(self, checking_obj: UserVoiceChat, control_obj: UserVoiceChat):
        for field in checking_obj.__dict__.keys():
            value = checking_obj.__dict__[field]
            controlValue = control_obj.__dict__[field]
            self.assertEqual(value, controlValue, '{2} should be {0} actual {1}'.format(controlValue, value, field))

    @classmethod
    def setUpClass(cls):
        UserService.add_new_user(101)
        print('\n[[[   TESTING UserVoiceChatService  ]]]\n')

    def setUp(self):
        UserVoiceChatService.clear_table()

    @classmethod
    def tearDownClass(cls):
        UserVoiceChatService.clear_table()
        UserService.clear_table()
    # =====================

    # =====================
    def test_add_new_user_voice_chat_and_get_by_user_id(self):
        print('Testing add_new_user_voice_chat() and get_user_voice_chat_by_user_id()')

        uChat = UserVoiceChat(userId=101, chatName='userChat', maxUsersCount=100)
        UserVoiceChatService.add_new_user_voice_chat(userVoiceChat=uChat)
        uChat2 = UserVoiceChatService.get_user_voice_chat_by_user_id(userId=101)

        self._check_data(checking_obj=uChat2, control_obj=uChat)
        print('Successful\n')
    # =====================

    # =====================
    def test_get_all_user_voice_chats(self):
        print('Testing get_all_user_voice_chats()')

        uChat = UserVoiceChat(userId=101, chatName='userChat', maxUsersCount=100)
        UserVoiceChatService.add_new_user_voice_chat(userVoiceChat=uChat)
        answer = UserVoiceChatService.get_all_user_voice_chats()

        self.assertEqual(1, len(answer), 'rowCount should be {0} actual {1}'.format(1, len(answer)))
        self._check_data(checking_obj=answer[0], control_obj=uChat)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_user_voice_chat(self):
        print('Testing update_user_voice_chat_by_user_id()')

        uChat = UserVoiceChat(userId=101, chatName='userChat', maxUsersCount=100)
        UserVoiceChatService.add_new_user_voice_chat(userVoiceChat=uChat)
        UserVoiceChatService.\
            update_user_voice_chat_by_user_id(UserVoiceChat(userId=101, chatName='myChat', maxUsersCount=10))
        uChat2 = UserVoiceChatService.get_user_voice_chat_by_user_id(userId=101)
        uChat.chatName = 'myChat'
        uChat.maxUsersCount = 10

        self._check_data(checking_obj=uChat2, control_obj=uChat)
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_user_voice_chat_by_user_id(self):
        print('Testing delete_user_voice_chat_by_user_id()')
        UserVoiceChatService.add_new_user_voice_chat(UserVoiceChat(userId=101, chatName='userChat'))
        UserVoiceChatService.delete_user_voice_chat_by_user_id(userId=101)

        answer = UserVoiceChatService.get_all_user_voice_chats()

        self.assertEqual(0, len(answer), 'rowCount should be {0} actual {1}'.format(0, len(answer)))
        print('Successful\n')


if __name__ == '__main__':
    print('boot unit tests')
    unittest.main()
