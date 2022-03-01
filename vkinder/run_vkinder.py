import os

from vkinder_finder import run

if __name__ == '__main__':
    TOKEN = os.getenv('vk_token')
    run(TOKEN)
