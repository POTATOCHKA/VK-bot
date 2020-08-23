


# engine = create_engine('sqlite:///bot.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# token_list = ['123']
# req_count = 0
# sock = socket.socket()
# sock.connect(('35.204.44.141', 2003))
# tokenVK = "af396eb188a1e8b5a3f9c7048a77cc58360b6c1f07de37308da65e1bd1afa1604d62ad344633cb223078f"
# tokenYA = 'trnsl.1.1.20191124T194816Z.0d0f5b45c30ce891.f04d5002ddaf11b88d920875a68cecbe347c9947'
# vk = vk_api.VkApi(token=tokenVK)
# longpoll = VkLongPoll(vk)
#
#
#
# class VkBot:
#
#     def __init__(self, user_id):
#         self._USER_ID = user_id
#         self._USERNAME = self._get_user_name_from_vk_id(user_id)
#
#     def _get_user_name_from_vk_id(self, user_id):
#         request = requests.get("https://vk.com/id" + str(user_id))
#         bs = bs4.BeautifulSoup(request.text, "html.parser")
#
#         user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
#
#         return user_name.split()[0]
#
#     @staticmethod
#     def _clean_all_tag_from_str(string_line):
#         """
#         Очистка строки stringLine от тэгов и их содержимых
#         :param string_line: Очищаемая строка
#         :return: очищенная строка
#         """
#         result = ""
#         not_skip = True
#         for i in list(string_line):
#             if not_skip:
#                 if i == "<":
#                     not_skip = False
#                 else:
#                     result += i
#             else:
#                 if i == ">":
#                     not_skip = True
#
#         return result
#
#
#
# def packYandex(text_msg):
#     url_trans = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
#     trans_option = {'key': tokenYA, 'lang': 'ru-en', 'text': text_msg}
#     webRequest = requests.get(url_trans, params=trans_option)
#     s = loads(webRequest.text, encoding='utf-8')
#     if s["code"] != 200:
#         raise Exception(f"Yandex api crash")
#     data = s["text"][0]
#     return data
#
#
# #     global req_count
# #     sleep(60)
# #     sock.send(f'hackathon.team3.backend.cnt {req_count} -1\n'.encode('utf-8'))
# #     print('sended')
# #     req_count = 0
#
# vk.get_api().mmessages.send(peer_id=send_id,
#                                   message=message)
#
# def write_msg(user_id, random_id, message):
#     vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id, "keyboard": open("keyboards/default.json", "r", encoding="UTF-8").read()})
#
#
# # # Основной цикл
# def main():
#     for event in longpoll.listen():
#
#         # Если пришло новое сообщение
#         if event.type == VkEventType.MESSAGE_NEW:
#
#             # Если оно имеет метку для меня( то есть бота)
#             if event.to_me:
#                 # global req_count
#                 # req_count = req_count + 1
#
#                 # Каменная логика ответа
#                 if session.query(User).filter(User.user_id == event.user_id).first():
#                     row = Log(user_id=event.user_id, text=event.text.strip())
#                     session.add(row)
#                     session.commit()
#                     try:
#                         print(packYandex(event.text))
#                     except (Exception) as e:
#                         print(e)
#                 elif event.text in token_list:
#                     user = User(user_id=event.user_id)
#                     session.add(user)
#                     session.commit()
#                     write_msg(event.user_id, event.random_id,
#                               f'{VkBot(event.user_id)._USERNAME}, теперь ты авторизован! Для того чтобы '
#                               f'найти похожии, просто введи id. Чтобы найти комплиментарные напиши /id id'
#                               f'чтобы найти по названию введди ?слово.'
#                               # f' Чтобы вернуть товары из смежной категориинапиши !id'
#                               )
#                 else:
#                     write_msg(event.user_id, event.random_id,
#                               f'Привет {VkBot(event.user_id)._USERNAME}! У тебя нет доступа, пришли мне токен')
#
#
# if __name__ == '__main__':
# #     t = threading.Thread(target=agregate)
# #     t.start()
#     main()


# try:
#     q = Server.packYandex("en-ru", event.text)
# except (Exception) as e:
#     self.send_message(event.user_id, event.random_id,
#                       'Бот временно не работает(\n'
#                       'Повторите попытку позже!')
# try:
#     kinopoisk(q)
#     self.photo_user(event.user_id, event.random_id,
#                     "Kinopoisk думает, что это:",
#                     'kinopoisk.jpg')
# except (Exception) as e:
#     self.send_message(event.user_id, event.random_id,
#                       'Kinopoisk умер( \n')
# try:
#     google(q)
#     self.photo_user(event.user_id, event.random_id,
#                     "Google надеется, что угадал:",
#                     'google.jpg')
# except (Exception) as e:
#     self.send_message(event.user_id, event.random_id,
#                       'google капут( \n')
