from config import vk_api_token
from server import Server


server = Server(vk_api_token, 'smetanka')
server.start()
