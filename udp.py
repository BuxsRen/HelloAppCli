import socket
import config
import json
import threading
import time
import gzip


class Udp:
    play = None
    client = None
    buf_size = 10240  # socket字节
    token = ""
    to_id = ""
    status = False

    def __init__(self,audio):
        self.play = audio
        self.host = config.Conf.get_config("udp", "host")
        self.port = int(config.Conf.get_config("udp", "port"))

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 初始化

    # 登录
    def login(self,id,token):
        self.to_id = id
        self.token = token
        data = '{"type": "login","token":"' + token + '"}'
        self.client.sendto(data.encode('utf-8'), (self.host, self.port))
        time.sleep(1)
        self.status = True
        threading.Thread(target=self.send).start()
        threading.Thread(target=self.receive_server_data).start()

    # 接收实时音频流
    def receive_server_data(self):
        while self.status:
            try:
                data, server_addr = self.client.recvfrom(self.buf_size)
                data = json.loads(data)
                if data["type"] == "call":
                    self.play.playing_stream.write(gzip.decompress(bytes.fromhex(data['data'])))  # 16进制 转 bytes 播放
            except Exception as e:
                print("audio receive",e)
                break

    # 推送实时音频流
    def send(self):
        while self.status:
            try:
                data = gzip.compress(self.play.recording_stream.read(1024)).hex()  # 取实时音频流 并将 bytes 转 16进制
                data = '{"toId":'+self.to_id+',"data":"' + data + '","type":"call"}'
                self.client.sendto(data.encode('utf-8'), (self.host, self.port))
            except Exception as e:
                print("audio send", e)
                break