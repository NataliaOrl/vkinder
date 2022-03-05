import unittest

from search_users import search_users
from test_data import photos_get, three_photo, user_interests, user_music, user_books, user, subscriptions


class Test_VKUser(unittest.TestCase):
    def test_get_user_info(self):
        user_profile = user
        user_interests = list(map(str.strip, user_profile.get('interests', '').split(',')))
        user_music = list(map(str.strip, user_profile.get('music', '').split(',')))
        user_books = list(map(str.strip, user_profile.get('books', '').split(',')))
        user_subscriptions = subscriptions
        user_subscriptions_list = []
        for subscription in user_subscriptions['items']:
            user_subscriptions_list.append(subscription['id'])
        self.assertEqual(user_subscriptions_list, [210627750])
        self.assertEqual(user_interests, ['спорт', 'здоровое питание', 'здоровый образ жизни', 'интерьер', 'живопись',
                                          'компьютерные игры', 'футбол'])
        self.assertEqual(user_music, ['Чайковский', 'Моцарт'])
        self.assertEqual(user_books, ['Грозовые ворота', 'Что делать?', 'S.T.A.L.K.E.R'])

    def test_get_three_photo(self):
        for people in photos_get:
            if len(people) == 3:
                self.assertEqual(people['url'], three_photo)

    def test_get_suitable_users(self):
        super_users = []
        suitable_users = search_users['items']  # провели поиск подходящих аккаунтов
        for people in suitable_users:  # поиск совпадений по интересам
            for el in list(map(str.strip, people.get('interests', '').split(','))):
                if el in user_interests:
                    super_users.append(people['id'])
        for people in suitable_users:  # поиск совпадений по музыке
            for el in list(map(str.strip, people.get('music', '').split(','))):
                if el in user_music:
                    super_users.append(people['id'])
        for people in suitable_users:  # поиск совпадений по книгам
            for el in list(map(str.strip, people.get('books', '').split(','))):
                if el in user_books:
                    super_users.append(people['id'])
        self.assertEqual(super_users, [266488015])


if __name__ == '__main__':
    unittest.main()
