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


def get_params_search(user_id):
    write_msg(user_id, 'Введите минимальный возраст будущего знакомого')
    user = user_id
    msg = bot_speak()[1]
    if msg.isdigit():
        min_age = int(msg)
        write_msg(user_id, 'Введите максимальный возраст будущего знакомого')
    msg = bot_speak()[1]
    if msg.isdigit():
        max_age = int(msg)
    return user, min_age, max_age


def get_city_params(user_id):
    write_msg(user_id, 'Введите название города, в котором будем искать знакомства')
    city = bot_speak()[1]
    return city
