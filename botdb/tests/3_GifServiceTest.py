import unittest
from botdb.services import GifService
from botdb.services import GifGroupService
from botdb.services import UserService
from botdb.entities.Gif import Gif
from botdb.entities.GifGroup import GifGroup


class TestUserService(unittest.TestCase):

    def _check_data(self, gif: Gif, groupId: int, gifUrl: str):
        self.assertEqual(groupId, gif.groupId,
                         'groupId should be {0} actual {1}'.format(groupId, gif.groupId))
        self.assertEqual(gifUrl, gif.gifUrl,
                         'gifUrl should be {0} actual {1}'.format(gifUrl, gif.gifUrl))

    @classmethod
    def setUpClass(cls):
        UserService.add_new_user(101)
        GifGroupService.add_new_gif_group_full(GifGroup(authorId=101, name='test', groupType='common', phrase='testing'))
        print('\n[[[   TESTING GifGroupService   ]]]\n')

    def setUp(self):
        GifService.clear_table()
        GifService.add_new_gif(Gif(groupId=1, gifUrl='url1'))
        GifService.add_new_gif(Gif(groupId=1, gifUrl='url2'))
        GifService.add_new_gif(Gif(groupId=1, gifUrl='url3'))
        GifService.add_new_gif(Gif(groupId=2, gifUrl='2url1'))

    @classmethod
    def tearDownClass(cls):
        GifService.clear_table()
        GifGroupService.clear_table()
        UserService.clear_table()
    # =====================

    # =====================
    def test_add_new_gif_and_get_all(self):
        print('Testing add_new_gif() and get_all()')
        GifService.add_new_gif(gif=Gif(groupId=2, gifUrl='2url2'))

        answer = GifService.get_all_gif()

        self.assertEqual(5, len(answer), 'rows_count should be {0} actual {1}'.format(5, len(answer)))
        self._check_data(answer[0], groupId=1, gifUrl='url1')
        self._check_data(answer[4], groupId=2, gifUrl='2url2')
        print('Successful\n')
    # =====================

    # =====================
    def test_get_gif_count_by_group_id(self):
        print('Testing get_gif_count_by_group_id()')

        answer = GifService.get_gif_count_by_group_id(groupId=1)

        self.assertEqual(3, answer, 'rows_count should be {0} actual {1}'.format(3, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_get_gif_by_group_id_and_index(self):
        print('Testing get_gif_by_group_id_and_index()')

        gif = GifService.get_gif(groupId=1, index=2)

        self._check_data(gif=gif, groupId=1, gifUrl='url2')
        print('Successful\n')
    # =====================

    # =====================
    def test_get_gif_page_by_group_id_and_index(self):
        print('Testing get_gif_page_by_group_id_and_index()')
        GifService.add_new_gif(Gif(groupId=1, gifUrl='url4'))

        gifsPage = GifService.get_gif_page(groupId=1, index=2)

        self._check_data(gif=gifsPage[0], groupId=1, gifUrl='url2')
        self._check_data(gif=gifsPage[2], groupId=1, gifUrl='url4')
        self.assertEqual(3, len(gifsPage), 'rows_count should be {0} actual {1}'.format(3, len(gifsPage)))
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_gif_group_id_and_index(self):
        print('Testing delete_gif_group_id_and_index()')
        GifService.add_new_gif(Gif(groupId=1, gifUrl='url2'))
        GifService.add_new_gif(Gif(groupId=1, gifUrl='url3'))

        GifService.delete_gif_by_group_id_and_index(groupId=1, index=2)
        gifsPage = GifService.get_all_gif()

        self._check_data(gif=gifsPage[0], groupId=1, gifUrl='url1')
        self._check_data(gif=gifsPage[1], groupId=1, gifUrl='url3')
        print('Successful\n')
    # =====================

    # =====================
    def test_get_random_gif_from_group(self):
        print('Testing get_random_gif_from_group()')


        answer = GifService.get_random_gif_from_group(groupId=1)
        print('answer:')
        print(answer)
        print('Successful\n')


if __name__ == '__main__':
    print('boot unit tests')
    unittest.main()
