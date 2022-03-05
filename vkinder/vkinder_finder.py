from base_bot import write_msg, bot_speak, get_params_search
from vk_user import VKUser
from vkinder_db import add_user_block, add_user_favor, register_user, create, FavorList, session, check_db_user


def get_user_info(token):
    user_id, message = bot_speak()
    if not check_db_user(user_id):
        register_user(user_id)
    params_search = get_params_search(user_id, message)
    vkuser = VKUser(token, *params_search)
    vkuser.authorize_by_token()
    vkuser.get_city(user_id)
    write_msg(user_id, 'Начинаю поиск. Пожалуйста, подождите.')
    vkuser.get_sex()
    user_profile = vkuser.get_user_profile()  # получили данные о профиле заказчика
    user_interests = list(map(str.strip, user_profile.get('interests', '').split(',')))
    user_music = list(map(str.strip, user_profile.get('music', '').split(',')))
    user_books = list(map(str.strip, user_profile.get('books', '').split(',')))
    user_subscriptions = vkuser.get_subscriptions(user_id)  # провели поиск подписок заказчика
    user_subscriptions_list = []
    for subscription in user_subscriptions['items']:
        user_subscriptions_list.append(subscription['id'])
    return user_id, vkuser, user_subscriptions_list, user_interests, user_music, user_books


def get_three_photo(dict_users, numb_user=3):
    for el in range(4, 0, -1):
        for id, photo in dict_users.items():
            if len(photo[1]) == numb_user and photo[0] == el:
                yield id, photo[1][0]['url'], photo[1][1]['url'], photo[1][2]['url']


def send_favorites(user_id):
    for user, photo in session.query(FavorList.user_id, FavorList.url_photo):
        n = photo.split(',')
        write_msg(user_id, f"Ссылка на страницу пользователя: https://vk.com/id{user}\n"
                           f"Фотографии пользователя с наибольшим количеством лайков:\n{n[0]}\n{n[1]}\n{n[2]}\n")


def send_photo(dict_users, user_id):
    photos = get_three_photo(dict_users)
    for i in photos:
        write_msg(user_id, f"Ссылка на страницу пользователя: https://vk.com/id{i[0]}\n"
                           f"Фотографии пользователя с наибольшим количеством лайков:\n{i[1]}\n{i[2]}\n{i[3]}\n"
                           "Вам нравятся эти фотографии?")
        answer = bot_speak()[1].lower()
        if answer in ('да', 'yes', 'y'):
            add_user_favor(i[0], (i[1], i[2], i[3]))
        else:
            add_user_block(i[0])
        write_msg(user_id, 'Продолжаем поиск?')
        answer = bot_speak()[1].lower()
        if answer not in ('да', 'yes', 'y'):
            write_msg(user_id, 'До свидания')
            break
    else:
        write_msg(user_id, 'Подходящие анкеты закончились\n'
                           'Желаете повторно посмотреть фотографии понравившихся пользователей?')
        answer = bot_speak()[1].lower()
        if answer in ('да', 'yes', 'y'):
            send_favorites(user_id)
        write_msg(user_id, 'До свидания')


def get_suitable_users(user_id, vkuser, user_subscriptions_list, user_interests, user_music, user_books):
    super_users = {}
    suitable_users = vkuser.search_users()
    for people in suitable_users:
        for subscription in user_subscriptions_list:
            if subscription in [x['id'] for x in vkuser.get_subscriptions(people['id'])['items']]:
                super_users[people['id']] = 4
        for el in list(map(str.strip, people.get('interests', '').split(','))):
            if el in user_interests and people['id'] not in super_users:
                super_users[people['id']] = 3
        for el in list(map(str.strip, people.get('music', '').split(','))):
            if el in user_music and people['id'] not in super_users:
                super_users[people['id']] = 2
        for el in list(map(str.strip, people.get('books', '').split(','))):
            if el in user_books and people['id'] not in super_users:
                super_users[people['id']] = 1
    dict_users = {}
    for id, priority in super_users.items():
        dict_users[id] = (priority, vkuser.get_top_photo(id))
    send_photo(dict_users, user_id)


def run(token):
    create()
    *user, = get_user_info(token)
    get_suitable_users(*user)
