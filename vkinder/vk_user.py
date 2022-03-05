import vk_api

from base_bot import get_city_params
from vkinder_db import check_db_favor, check_db_block

'''Получаем параметры поиска из аккаунта пользователя'''


class VKUser:
    def __init__(self, token, id, age_from=18, age_to=18):
        self.token = token
        self.id = id
        self.age_from = age_from
        self.age_to = age_to

    def authorize_by_token(self):
        vk_session = vk_api.VkApi(token=self.token)
        vk = vk_session.get_api()
        self.VK = vk

    def get_city(self, user_id):
        try:
            self.city = self.VK.users.get(user_ids=self.id, fields='city')[0]['city']['id']
        except KeyError:
            self.city = self.VK.database.getCities(country_id=1, q=get_city_params(user_id))['items'][0]['id']
        return self.city

    def get_sex(self):
        sex = self.VK.users.get(user_ids=self.id, fields='sex')[0]['sex']
        if sex == 1:
            self.sex = 2
        else:
            self.sex = 1
        return self.sex

    def search_users(self, count=100):
        result = []
        for year in range(self.age_from, self.age_to + 1):
            search = self.VK.users.search(count=count, fields='books,interests,music',
                                          age_from=year, age_to=year, city=self.city, sex=self.sex,
                                          friend_status=0, relation=1)
            for people in search['items']:
                if (not (check_db_favor(people['id']) or check_db_block(people['id']))) \
                        and not people['is_closed']:
                    result += [people]
        return result

    def get_subscriptions(self, user_id):
        result = self.VK.users.getSubscriptions(user_id=user_id, extended=1, count=50)
        return result

    def get_user_profile(self):
        result = self.VK.users.get(user_ids=self.id, fields='books,interests,music')[0]
        return result

    def get_vk_users_photo(self, result, my_list):
        for i in result['items']:
            url = i['sizes'][len(i['sizes']) - 1]['url']
            likes = i['likes']['count']
            my_list.append({
                'url': url,
                'likes': likes
            })

    def get_top_photo(self, user_id, num=3):
        result = self.VK.photos.get(owner_id=user_id, album_id='profile', extended=True)
        result_2 = self.VK.photos.getUserPhotos(owner_id=user_id, extended=1)
        my_list = list()
        self.get_vk_users_photo(result, my_list)
        self.get_vk_users_photo(result_2, my_list)
        my_list = sorted(my_list, key=lambda x: x['likes'], reverse=True)
        if len(my_list) > num:
            my_list = my_list[:num]
        return my_list
