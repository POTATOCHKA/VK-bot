
# Импортируем созданный нами класс Server
from server import Server
from config import vk_api_token



server1 = Server(vk_api_token, server_name="server1")
server1.start()