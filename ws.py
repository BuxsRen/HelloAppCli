import config
from websocket import create_connection # pip install websocket,websocket_client
import json
import threading

class WebSocket:
    ws = None

    def __init__(self,token,user):
        self.token = token
        self.user = user

    # 连接websocket服务
    def connect(self):
        self.ws = create_connection(config.Conf.get_config("config","ws") + "?token=" + self.token)
        threading.Thread(target=self.receive_server_data).start() # 开启接收线程

    # 接收消息
    def receive_server_data(self):
        while True:
            try:
                data = self.ws.recv()
                data = json.loads(data)
                if data["type"] == "ping":
                    continue

                self.user.msg(data)
            except Exception as e:
                print("WebSocket断开连接")
                exit(0)

    # 发送json数据
    def send(self,data):
        self.ws.send(data)
