import unittest

from search_users import search_users, result_search_users
from test_data import sex


class Test_VK_user(unittest.TestCase):
    def setUp(self):
        self.sex = sex
        self.profile = {'id': 110468543, 'first_name': 'Ольга', 'last_name': 'Иванова',
                        'can_access_closed': True, 'is_closed': True,
                        'interests': 'спорт, здоровое питание, здоровый образ жизни, интерьер, живопись,'
                                     ' компьютерные игры, футбол',
                        'books': 'Грозовые ворота, Что делать?, S.T.A.L.K.E.R', 'music': 'Чайковский, Моцарт'}

    def tearDown(self):
        pass

    def test_get_sex(self):
        sex = self.sex
        if sex == 1:
            self.sex = 2
            self.assertEqual(self.sex, 2)
        else:
            self.sex = 1
            self.assertEqual(self.sex, 1)

    def test_search_users(self):
        result = []
        search = search_users
        for people in search['items']:
            result += [people]
        self.assertEqual(result, result_search_users)


if __name__ == '__main__':
    unittest.main()
