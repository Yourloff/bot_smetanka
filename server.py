import vk_api.vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboardButton, VkKeyboardColor, VkKeyboard
from bot import Bot


class Server:
    API_VERSION = '5.154'
    START = 'Записаться'

    def __init__(self, api_token, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token, api_version=self.API_VERSION)
        self.long_poll = VkLongPoll(self.vk)
        self.vk_api = self.vk.get_api()
        self.vk_upload = vk_api.VkUpload(self.vk)

    def payload_data(self, data):
        parsed_data = json.loads(data)
        return parsed_data['command']

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                bot = Bot(user_id=event.user_id, vk_api=self.vk_api, vk_upload=self.vk_upload)

                if event.message == self.START:
                    bot.create_user()

                if bot.user_exist():
                    try:
                        message = self.payload_data(event.payload)
                    except AttributeError:
                        message = event.message

                    bot.say()
                    bot.request(message)
                else:
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button(self.START, color=VkKeyboardColor.PRIMARY)
                    bot.send_keyboard(keyboard, message=f"Нажмите '{self.START}', для проведения краткого "
                                                        "анкетирования")
