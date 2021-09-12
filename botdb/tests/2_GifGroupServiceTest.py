import unittest
from botdb.services import GifGroupService
from botdb.services import UserService
from botdb.entities.GifGroup import GifGroup


class TestGifGroupService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        UserService.add_new_user(10101)
        print('\n[[[   TESTING GifGroupService   ]]]\n')

    def setUp(self):
        GifGroupService.clear_table()
        gifGroup = GifGroup(authorId=10101, name='test0', createDate='2021-09-08',
                            groupType='common', phrase='testing0')
        GifGroupService.add_new_gif_group_full(gifGroup=gifGroup)

    @classmethod
    def tearDownClass(cls):
        GifGroupService.clear_table()
        UserService.clear_table()
    # =====================

    # =====================
    def _check_data(self, checking_obj: GifGroup, control_obj: GifGroup):
        for field in checking_obj.__dict__.keys():
            value = checking_obj.__dict__[field]
            controlValue = control_obj.__dict__[field]
            self.assertEqual(value, controlValue, '{2} should be {0} actual {1}'.format(controlValue, value, field))
    # =====================

    # =====================
    def test_add_new_gif_group_and_get_gif_group_by_id(self):
        print('Testing test_add_new_gif_group() and get_gif_group_by_id()')

        gifGroup = GifGroup(groupId=2, authorId=10101,  createDate='2021-09-08',
                            accessLevel=0, groupType='common', name='test1')
        GifGroupService.add_new_gif_group(gifGroup=GifGroup(authorId=10101, createDate='2021-09-08', name='test1'))
        gifGroup2 = GifGroupService.get_gif_group_by_id(2)

        self._check_data(checking_obj=gifGroup2, control_obj=gifGroup)
        print('Successful\n')
    # =====================

    # =====================
    def test_add_new_gif_group_full(self):
        print('Testing add_new_gif_group_full()')

        gifGroup = GifGroup(authorId=10101, createDate='2021-09-08', name='test2', groupType='common', phrase='testing')
        GifGroupService.add_new_gif_group_full(gifGroup=gifGroup)
        gifGroup = GifGroup(groupId=2, authorId=10101, createDate='2021-09-08',
                            accessLevel=0, groupType='common', name='test2', phrase='testing')
        gifGroup2 = GifGroupService.get_gif_group_by_id(2)

        self._check_data(checking_obj=gifGroup2, control_obj=gifGroup)
        print('Successful\n')
    # =====================

    # =====================
    def test_get_gif_group_by_name(self):
        print('Testing get_gif_group_by_name()')

        gifGroup = GifGroupService.get_gif_group_by_name('test0')
        self._check_data(checking_obj=gifGroup,
                         control_obj=GifGroup(groupId=1, authorId=10101,  createDate='2021-09-08',
                                              accessLevel=0, groupType='common', name='test0', phrase='testing0'))
        print('Successful\n')
    # =====================

    # =====================
    def test_get_all_gif_groups(self):
        print('Testing get_all_gif_groups()')

        answer = len(GifGroupService.get_all_gif_groups())

        self.assertEqual(1, answer, 'phrase should be {0} actual {1}'.format(1, answer))
        print('Successful\n')
    # =====================

    # =====================
    # def test_get_gif_groups_by_type(self):
    #     print('Testing get_all_gif_groups()')
    #     gifGroup = GifGroup(authorId=10101, name='test1', createDate='2021-09-08',
    #                         groupType='common', phrase='testing1')
    #     GifGroupService.add_new_gif_group_full(gifGroup=gifGroup)
    #     gifGroup = GifGroup(authorId=10101, name='test2', createDate='2021-09-08',
    #                         groupType='system', phrase='testing1')
    #     GifGroupService.add_new_gif_group_full(gifGroup=gifGroup)
    #     GifGroupService.update_gif_group(gifGroup=gifGroup)
    #
    #     groupList = GifGroupService.get_all_gif_groups()
    #     for group in groupList:
    #         print(group)
    #
    #     answer = len(GifGroupService.get_gif_groups_by_type(groupType='common'))
    #
    #     self.assertEqual(2, answer, 'phrase should be {0} actual {1}'.format(2, answer))
    #     print('Successful\n')
    # =====================

    # =====================
    def test_update_gif_group(self):
        print('Testing update_gif_group()')

        gifGroup = GifGroupService.get_gif_group_by_id(1)
        gifGroup.name = 'Test2'
        gifGroup.phrase = 'wow'
        gifGroup.accessLevel = 1
        GifGroupService.update_gif_group(gifGroup=gifGroup)
        gifGroup2 = GifGroupService.get_gif_group_by_id(1)

        self._check_data(checking_obj=gifGroup2, control_obj=gifGroup)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_gif_group_access_level(self):
        print('Testing update_gif_group_access_level()')

        gifGroup = GifGroupService.get_gif_group_by_id(1)
        gifGroup.accessLevel = 1
        GifGroupService.update_gif_group_access_level(gifGroup=gifGroup)
        gifGroup2 = GifGroupService.get_gif_group_by_id(1)

        self._check_data(checking_obj=gifGroup2, control_obj=gifGroup)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_gif_group_phrase(self):
        print('Testing update_gif_group_phrase()')

        gifGroup = GifGroupService.get_gif_group_by_id(1)
        gifGroup.phrase = 'hello'
        GifGroupService.update_gif_group_phrase(gifGroup=gifGroup)
        gifGroup2 = GifGroupService.get_gif_group_by_id(1)

        self._check_data(checking_obj=gifGroup2, control_obj=gifGroup)
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_by_id(self):
        print('Testing delete_gif_group_by_id()')

        GifGroupService.delete_gif_group_by_id(1)
        answer = len(GifGroupService.get_all_gif_groups())

        self.assertEqual(0, answer, 'phrase should be {0} actual {1}'.format(0, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_by_name(self):
        print('Testing delete_gif_group_by_id()')

        GifGroupService.delete_gif_group_by_name('test0')
        answer = len(GifGroupService.get_all_gif_groups())

        self.assertEqual(0, answer, 'phrase should be {0} actual {1}'.format(0, answer))
        print('Successful\n')


if __name__ == '__main__':
    print('boot unit tests')
    unittest.main()
