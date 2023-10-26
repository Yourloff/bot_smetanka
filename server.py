import vk_api.vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from bot import Bot


class Server:
    API_VERSION = '5.154'

    def __init__(self, api_token, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token, api_version=self.API_VERSION)
        self.long_poll = VkLongPoll(self.vk)
        self.vk_api = self.vk.get_api()

    def payload_data(self, data):
        parsed_data = json.loads(data)
        return parsed_data['command']

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                bot = Bot(user_id=event.user_id, vk_api=self.vk_api)
                try:
                    message = self.payload_data(event.payload)
                except AttributeError as e:
                    print(f"Ошибка: {e}")
                    message = event.message

                bot.request(message)
