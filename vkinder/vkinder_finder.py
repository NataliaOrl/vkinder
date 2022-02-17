from base_bot import write_msg, bot_speak, get_params_search
from vk_user import VK_user
from vkinder_db import add_user_block, add_user_favor, send_favorites, create, drop


def get_user_info(token):
    user_id, message = bot_speak()
    params_search = get_params_search(user_id, message)
    vkuser = VK_user(token, *params_search)
    vkuser.authorize_by_token()
    vkuser.get_city()
    vkuser.get_sex()
    user_profile = vkuser.get_user_profile()  # получили данные о профиле заказчика
    user_interests = list(map(str.strip, user_profile.get('interests', '').split(',')))
    user_music = list(map(str.strip, user_profile.get('music', '').split(',')))
    user_books = list(map(str.strip, user_profile.get('books', '').split(',')))
    user_Subscriptions = vkuser.get_Subscriptions(user_id)  #  провели поиск подписок заказчика
    user_Subscriptions_list = []
    for subscription in user_Subscriptions['items']:
        user_Subscriptions_list.append(subscription['id'])
    return user_id, vkuser, user_Subscriptions_list, user_interests, user_music, user_books 

def get_three_photo(dict_users):
    for id, people in dict_users.items():
        if len(people) == 3:
            yield (id, people[0]['url'], people[1]['url'], people[2]['url'])

def send_photo(dict_users, user_id, vkuser, user_Subscriptions_list, user_interests, user_music, user_books): # отправка фото
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
        write_msg(user_id, 'Подходящие анкеты закончились\nПровести повторный поиск?')
        answer = bot_speak()[1].lower()
        if answer in ('да', 'yes', 'y'):
            get_suitable_users(user_id, vkuser, user_Subscriptions_list, user_interests, user_music, user_books)
        else:
            write_msg(user_id, 'Желаете повторо посмотреть фотографии понравившихся пользователей?')
            answer = bot_speak()[1].lower()
            if answer not in ('да', 'yes', 'y'):
                write_msg(user_id, 'До свидания')
            else:
                send_favorites(user_id)
                write_msg(user_id, 'До свидания')         

def get_suitable_users(user_id, vkuser, user_Subscriptions_list, user_interests, user_music, user_books):
    super_users = []
    suitable_users = vkuser.search_users()   # провели поиск подходящих аккаунтов 
    for people in suitable_users:           #  поиск совпадений по подпискам
        if not people['is_closed'] and vkuser.get_Subscriptions(people['id']) in user_Subscriptions_list:
            super_users.append(people['id'])
    for people in suitable_users:          #  поиск совпадений по интересам
        for el in list(map(str.strip, people.get('interests', '').split(','))):
            if el in user_interests:
                super_users.append(people['id'])  
    for people in suitable_users:          #  поиск совпадений по музыке
        for el in list(map(str.strip, people.get('music', '').split(','))):
            if el in user_music:
                super_users.append(people['id'])
    for people in suitable_users:          #  поиск совпадений по книгам
        for el in list(map(str.strip, people.get('books', '').split(','))):
            if el in user_books:
                super_users.append(people['id'])
    dict_users = {}
    for people in super_users:  
        dict_users[people] = vkuser.get_top_photo(people)
    send_photo(dict_users, user_id, vkuser, user_Subscriptions_list, user_interests, user_music, user_books)

def run(token):
    drop()
    create()  
    *user, = get_user_info(token)
    get_suitable_users(*user)


