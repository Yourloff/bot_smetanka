import json
import os
import random


class Bot:
    DIRECTORY = 'user_responses'

    def __init__(self, user_id, vk_api, vk_upload):
        self.user_id = user_id
        self.vk_api = vk_api
        self.upload = vk_upload
        self.PATH = os.path.join(self.DIRECTORY, str(self.user_id) + '.json')
        self.DATASET = 'dataset.json'

    def get_user_name(self):
        return self.vk_api.users.get(user_id=self.user_id)[0]['first_name']

    def send_msg(self, message):
        if message is not None:
            random_id = random.getrandbits(31)
            self.vk_api.messages.send(peer_id=self.user_id,
                                      message=message,
                                      random_id=random_id)

    def send_keyboard(self, keyboard, message):
        random_id = random.getrandbits(31)
        self.vk_api.messages.send(peer_id=self.user_id, message=message, keyboard=keyboard.get_keyboard(),
                                  random_id=random_id)

    def send_photo(self):
        random_id = random.getrandbits(31)
        file_path = os.path.join('img', 'hairstyle.jpg')
        photo = self.upload.photo_messages(file_path)
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self.vk_api.messages.send(peer_id=self.user_id,
                                  attachment=attachment,
                                  random_id=random_id)

    def say(self):
        user_res = self.read_json(self.PATH)
        list_user_res = list(user_res.keys())
        dataset = self.read_json(self.DATASET)
        list_data = list(dataset['questions'])

        for dataset_key in list_data:
            if dataset_key in list_user_res:
                continue
            elif type(dataset['questions'][dataset_key]) == list:
                for item in dataset['questions'][dataset_key]:
                    for key, value in item.items():
                        if key == 'attachment':
                            self.send_photo()
                        else:
                            self.send_msg(value)
                user_res[dataset_key] = "Фото отправлено"
                self.append_user_file(user_res)
            else:
                user_res[dataset_key] = ""
                self.append_user_file(user_res)
                self.send_msg(dataset['questions'][dataset_key].replace('username', self.get_user_name()))
                break

    def create_user(self):
        self.create_file_answers()
        text = self.read_dataset('start')
        self.send_msg(text.replace('username', self.get_user_name()))

    def answer(self, message):
        user_res = self.read_json(self.PATH)

        for key in user_res:
            if user_res[key] == '':
                user_res[key] = message
                self.append_user_file(user_res)

    def request(self, message):
        self.answer(message)

    def user_exist(self):
        return os.path.isfile(self.PATH)

    def read_json(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            file.close()
            return data

    def read_dataset(self, key):
        try:
            with open('dataset.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                file.close()
                return data[key]
        except TypeError as e:
            print(f"Ошибка типа данных: {e}")
            return None
        except KeyError as e:
            print(f"Ключ не найден в данных: {e}")
            return None

    def append_user_file(self, data):
        with open(self.PATH, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.close()

    def create_file_answers(self):
        if not os.path.exists(self.DIRECTORY):
            os.mkdir(self.DIRECTORY)

        with open(self.PATH, 'w', encoding='utf-8') as f:
            data = {
                'link': 'https://vk.com/id' + str(self.user_id)
            }

            json_string = json.dumps(data, ensure_ascii=False)
            f.write(json_string)
            f.close()
        print('Файл для ' + self.get_user_name() + ' (' + str(self.user_id) + ') создан!')
