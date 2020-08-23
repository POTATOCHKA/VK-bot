import vk_api.vk_api
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from models import Base, User, Log
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from json import loads
from config import tokenYA, token_list
from parse import kinopoisk
import json
import Film
import vino
import model
import Mail

engine = create_engine('sqlite:///bot.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Server:

    def __init__(self, api_token, server_name: str = "Empty"):
        # Даем серверу имя
        self.server_name = server_name

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self.long_poll = VkLongPoll(self.vk)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, message):
        """
        Отправка сообщения через метод messages.send
        :param send_id: vk id пользователя, который получит сообщение
        :param message: содержимое отправляемого письма
        :return: None
        """
        self.vk_api.messages.send(peer_id=send_id,
                                  message=message)

    def start(self):
        global q
        global mode
        global vino_dict
        global mail_dict
        vino_dict = vino.Bot()
        eat_dict = model.FoodGetter()
        mail_dict = Mail.wise_bot()
        eat_dict.load("ingredients.csv", "doc2vec_model", "annoy_model_")
        mode = {}
        q = 0
        print('всё подгрузил')

        for event in self.long_poll.listen():  # Слушаем сервер

            # Пришло новое сообщение
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                q += 1

                username = self.get_user_name(event.user_id)
                if session.query(User).filter(
                        User.user_id == event.user_id).first():
                    Server.user_log(event.user_id, event.text)
                    if event.user_id not in mode:
                        mode[event.user_id] = [0]
                    print(mode)
                    if mode[event.user_id][0] == 3 and event.text == \
                            'Красное вино':
                        vino_red = mode[event.user_id][1]
                        for i in range(len(vino_red[1])):
                            if i < 5:
                                self.send_message(event.user_id, event.random_id,
                                                  vino_red[1][i]['name'] +
                                                  ", " + vino_red[1][i][
                                                      'sugar'] + ', ' +
                                                  str(vino_red[1][i][
                                                          'rating']))
                            else:
                                break
                        self.send_message(event.user_id, event.random_id,
                                          'Это выборка красного вина',
                                          keyboard="keyboard.json")
                        mode[event.user_id][0] = 0
                        continue
                    elif mode[event.user_id][0] == 3 and event.text == \
                            'Белое ' \
                            'вино':
                        vino_white = mode[event.user_id][1]
                        for i in range(len(vino_white[2])):
                            if i < 5:
                                self.send_message(event.user_id, event.random_id,
                                                  vino_white[2][i]['name'] +
                                                  ", " + vino_white[2][i][
                                                      'sugar'] + ', ' +
                                                  str(vino_white[2][i][
                                                          'rating']))
                            else:
                                break
                        self.send_message(event.user_id, event.random_id,
                                          'Это выборка белого вина',
                                          keyboard="keyboard.json")
                        mode[event.user_id][0] = 0
                        continue
                    if mode[event.user_id][0] == 3 and event.text == \
                            'Розовое ' \
                            'вино':
                        vino_pink = mode[event.user_id][1]
                        if len(vino_pink[3]) == 0:
                            self.send_message(event.user_id, event.random_id,
                                              'Нет винишка', keyboard="keyboard.json")
                            mode[event.user_id][0] = 0
                            continue
                        for i in range(len(vino_pink[3])):
                            if i < 5:
                                self.send_message(event.user_id, event.random_id,
                                                  vino_pink[3][i]['name'] +
                                                  ", " + vino_pink[3][i][
                                                      'sugar'] + ', ' +
                                                  str(vino_pink[3][i][
                                                          'rating']))
                            else:
                                break
                        self.send_message(event.user_id, event.random_id,
                                          'Это выборка розового вина',
                                          keyboard="keyboard.json")
                        mode[event.user_id][0] = 0
                        continue
                    if mode[event.user_id][0] == 3 and event.text == 'Другие ' \
                                                                     'функции':
                        self.send_message(event.user_id,
                                          event.random_id, 'Выбирай '
                                                           'что-то',
                                          keyboard='keyboard.json')
                        mode[event.user_id][0] = 0
                        continue
                    elif mode[event.user_id][0] == 1 and event.text == \
                            'Другие функции':
                        self.send_message(event.user_id,
                                          event.random_id, 'Выбирай '
                                                           'что-то',
                                          keyboard='keyboard.json')
                        mode[event.user_id][0] = 0
                        continue
                    elif mode[event.user_id][0] == 1:
                        if len(event.text) > 70:
                            self.send_message(event.user_id, event.random_id,
                                              'Многа букав',
                                              keyboard="keyboard.json")
                            mode[event.user_id][0] = 0
                        else:
                            try:
                                user_film = self.packYandex('ru-en', event.text)
                            except (Exception) as e:
                                self.send_message(event.user_id, event.random_id,
                                                  'Yandex умер( \n')
                            print(user_film)
                            films = Film.film_advice().give_film(str(user_film))
                            if films[0] == "incorrect request":
                                self.send_message(event.user_id, event.random_id,
                                                  "Фильмы закончились",
                                                  keyboard='keyboard2.json')
                                mode[event.user_id][0] = 0
                            else:
                                for i in films:
                                    try:
                                        message = self.packYandex('en-ru', i)
                                    except (Exception) as e:
                                        self.send_message(event.user_id,
                                                          event.random_id,
                                                          'Yandex умер( \n')
                                    try:
                                        kinopoisk(i)
                                    except (Exception) as e:
                                        self.send_message(event.user_id,
                                                          event.random_id,
                                                          'Кинопоиск крякнул( \n')
                                    self.photo_user(event.user_id, event.random_id,
                                                    'Оригинальное название: '
                                                    + i + '\nПереведенное '
                                                          'название: ' + message,
                                                    'kinopoisk.jpg')
                                self.send_message(event.user_id, event.random_id,
                                                  "\nKinopoisk " +
                                                  "думает, что это:",
                                                  keyboard='keyboard2.json')
                    elif mode[event.user_id][0] == 2 and event.text == \
                            'Другие ' \
                            'функции':
                        self.send_message(event.user_id, event.random_id, 'Выбирай что-то', keyboard='keyboard.json')
                        mode[event.user_id][0] = 0
                    elif mode[event.user_id][0] == 2:
                        if len(event.text) > 70:
                            self.send_message(event.user_id, event.random_id,
                                              'Многа букав',
                                              keyboard="keyboard.json")
                            mode[event.user_id][0] = 0
                        else:
                            try:
                                text = self.packYandex('ru-en', event.text)
                            except (Exception) as e:
                                self.send_message(event.user_id,
                                                  event.random_id,
                                                  'Yandex умер( \n')
                            Server.user_log(event.user_id, event.text)
                            temp = eat_dict.find(text, 5)
                            if len(temp) == 0:
                                self.send_message(event.user_id, event.random_id,
                                                  'Останешься голодным или попробуй ввести больше ингридиентов',
                                                  keyboard="keyboard2.json")
                                mode[event.user_id][0] = 2
                            else:
                                for i, j, _id in eat_dict.find(text, 5):
                                    i = self.packYandex('en-ru', i)
                                    j = self.packYandex('en-ru', j)
                                    self.send_message(event.user_id, event.random_id,
                                                      i + ":  " + j)
                                self.send_message(event.user_id, event.random_id,
                                                  'Кушай на здоровье!',
                                                  keyboard="keyboard2.json")
                    elif mode[event.user_id][0] == 3:
                        if len(event.text) > 70:
                            self.send_message(event.user_id, event.random_id,
                                              'Многа букав',
                                              keyboard="keyboard.json")
                            mode[event.user_id][0] = 0
                        else:
                            try:
                                vino_all = vino_dict.find_buchlo(
                                    event.text)
                                if len(mode[event.user_id]) == 1:
                                    mode[event.user_id].append(vino_all)
                                else:
                                    mode[event.user_id][1] = vino_all
                                for i in range(5):
                                    self.send_message(event.user_id,
                                                      event.random_id,
                                                      vino_all[0][i]['name'] +
                                                      ", " + vino_all[0][i][
                                                          'sugar'] + ', ' +
                                                      str(vino_all[0][i][
                                                              'rating']))
                                self.send_message(event.user_id, event.random_id,
                                                  'Это общая выборка вин',
                                                  keyboard="keyboard1.json")
                            except:
                                self.send_message(event.user_id, event.random_id,
                                                  'Сегодня ты трезвый!',
                                                  keyboard='keyboard.json')
                                mode[event.user_id][0] = 0


                    elif mode[event.user_id][0] == 0 and event.text == \
                            "Описание фильма":
                        self.send_message(event.user_id, event.random_id,
                                          f'{username}, опиши фильм!')
                        mode[event.user_id][0] = 1

                    elif mode[event.user_id][0] == 0 and event.text == \
                            "Описание еды":
                        self.send_message(event.user_id, event.random_id,
                                          f'{username}, опиши еду!')
                        mode[event.user_id][0] = 2



                    elif mode[event.user_id][0] == 0 and event.text == \
                            "Описание вина":
                        self.send_message(event.user_id, event.random_id,
                                          f'{username}, опиши вино!')
                        mode[event.user_id][0] = 3


                    else:
                        if len(event.text) > 70:
                            self.send_message(event.user_id, event.random_id,
                                              'Многа букав',
                                              keyboard="keyboard.json")
                            mode[event.user_id][0] = 0
                        else:
                            mas = mail_dict.give_answer(event.text)
                            if mas[0] == 'incorrect request':
                                self.send_message(event.user_id, event.random_id,
                                                  'https://vk.com/video?z=video273519762_456239269%2Fpl_cat_updates',
                                                  keyboard="keyboard.json")
                                mode[event.user_id][0] = 0
                            else:
                                if len(mas[0]) > 4000:
                                    self.send_message(event.user_id, event.random_id,
                                                      'Слишком длинное сообщение для вк',
                                                      keyboard="keyboard.json")
                                    mode[event.user_id][0] = 0
                                else:
                                    self.send_message(event.user_id, event.random_id,
                                                      mas[0],
                                                      keyboard="keyboard.json")
                                    mode[event.user_id][0] = 0


                elif event.text in token_list:
                    user = User(user_id=event.user_id)
                    session.add(user)
                    session.commit()
                    self.send_message(event.user_id, event.random_id,
                                      'https://vk.com/video?q=welcom%20to%20the%20club&z=video171354828_171644015')
                    self.send_message(event.user_id, event.random_id,
                                      f'{username}, теперь ты авторизован!',
                                      keyboard='keyboard.json')
                    self.photo_user(event.user_id, event.random_id,'Оригинальное название: ', 'kinopoisk.jpg')

                else:
                    self.send_message(event.user_id, event.random_id,
                                      'https://vk.com/videos147211044?z=video-145643494_456243932%2Fpl_147211044_-2')
                    self.send_message(event.user_id, event.random_id,
                                      f'Привет, {username}! У тебя нет доступа, пришли мне токен!')

    def get_user_name(self, user_id):
        """ Получаем имя пользователя"""
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    def get_user_city(self, user_id):
        """ Получаем город пользователя"""
        return \
            self.vk_api.users.get(user_id=user_id, fields="city")[0]["city"][
                'title']

    def photo_user(self, user_id, random_id, message, filename):
        data = self.vk_api.photos.getMessagesUploadServer(user_id=-190332116)
        print(data)

        upload_url = data["upload_url"]
        files = {'photo': open(filename, 'rb')}

        response = requests.post(upload_url, files=files)
        result = json.loads(response.text)
        print(result)
        uploadResult = self.vk_api.photos.saveMessagesPhoto(
            server=result["server"],
            photo=result["photo"],
            hash=result["hash"])

        self.vk_api.messages.send(user_id=user_id,
                                  random_id=random_id,
                                  message=message,
                                  attachment='photo-190332116_' +
                                             str(uploadResult[0]["id"]))

    def send_message(self, peer_id, random_id, message, keyboard=None):
        if keyboard is not None:
            self.vk_api.messages.send(peer_id=peer_id, random_id=random_id,
                                      message=message,
                                      keyboard=open(keyboard, "r",
                                                    encoding="UTF-8").read())
        if keyboard is None:
            self.vk_api.messages.send(peer_id=peer_id, random_id=random_id,
                                      message=message)

    @staticmethod
    def packYandex(len, text_msg):
        url_trans = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        if len == 'ru-en':
            trans_option = {'key': tokenYA, 'lang': 'ru-en', 'text': text_msg}
            webRequest = requests.get(url_trans, params=trans_option)
            s = loads(webRequest.text, encoding='utf-8')
            if s["code"] != 200:
                raise Exception(f"Yandex api crash")
            data = s["text"][0]
            return data
        elif len == "en-ru":
            trans_option = {'key': tokenYA, 'lang': 'en-ru', 'text': text_msg}
            webRequest = requests.get(url_trans, params=trans_option)
            s = loads(webRequest.text, encoding='utf-8')
            if s["code"] != 200:
                raise Exception(f"Yandex api crash")
            data = s["text"][0]
            return data

    @staticmethod
    def user_log(user_id, text):
        row = Log(user_id=user_id, text=text.strip(

        ), date=datetime.datetime.now().strftime("%Y-%m-%d "
                                                 "%H:%M:%S"))
        session.add(row)
        session.commit()

    @staticmethod
    def last_query(user_id):
        print(session.query(Log).get(user_id))
