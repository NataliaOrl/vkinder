import os

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

KEY_VK = os.getenv('key_vk')
session = vk_api.VkApi(token=KEY_VK)


def write_msg(user_id, message):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0
    }
    session.method("messages.send", post)


def bot_speak():
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.lower()
            user_id = event.user_id
            return user_id, text


def get_params_search(user_id, message):
    if message in ('привет', 'здравствуй', 'hello', 'hi', 'заново', 'restart'):
        write_msg(user_id, 'Добро пожаловать в самое лучшее приложение для знакомств!\n'
                           'Введите минимальный возраст будущего знакомого')
    user = user_id
    msg = ''
    while not msg.isdigit():
        msg = bot_speak()[1]
        if msg.isdigit():
            min_age = int(msg)
            write_msg(user_id, 'Введите максимальный возраст будущего знакомого')
        else:
            write_msg(user_id, 'Введите корректный минимальный возраст будущего знакомого')
    msg = ''
    while not msg.isdigit():
        msg = bot_speak()[1]
        if msg.isdigit():
            max_age = int(msg)
        else:
            write_msg(user_id, 'Введите корректный максимальный возраст будущего знакомого')
    if min_age > max_age:
        max_age, min_age = min_age, max_age
    return user, min_age, max_age


def get_city_params(user_id):
    write_msg(user_id, 'Введите название города, в котором будем искать знакомства')
    city = None
    while not city:
        answer = bot_speak()[1]
        if ''.join(answer.split(' ')).isalpha() or ''.join(answer.split('-')).isalpha():
            city = answer
        else:
            write_msg(user_id, 'Введите правильно название города, в котором будем искать знакомства')
    return city
