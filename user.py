import audio
import request
import udp
import ws
import time


class User:
    ws_client = None
    id = 0
    token = ""
    username = ""
    nickname = ""
    avatar = ""
    sex = 0
    req = None
    list = {}
    socket = None

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.req = request.Request()

    def login(self):
        res = self.req.post("/api/login",{"username": self.username,"password": self.password})
        if res["code"] == 200:
            print("√",res["msg"])
            data = res["data"]
            self.id = data["id"]
            self.token = data["token"]
            self.nickname = data["nickname"]
            self.avatar = data["avatar"]
            self.sex = data["sex"]
            self.username = data["username"]

            self.req.set_header("id", self.token)

            self.get_list()

            self.ws_client = ws.WebSocket(self.token,self)
            self.ws_client.connect()
        else:
            print(res["msg"])

    # 处理websocket消息
    def msg(self,data):
        if data["type"] == "login":
            if data["from"] == self.id:
                return
            else:
                print("用户[%s]上线了" % data["from"])
            return

        if data["type"] == "logout":
            if data["from"] == self.id:
                print(data["data"])
            else:
                print("用户[%s]离线了" % data["from"])
            return

        if data["type"] == "list":
            print("在线用户:",data["data"])
            return

        # 来电
        if data["type"] == "hangUp" and data["from"] != self.id:
            print(self.list[data["from"]]["nickname"] + "挂断了语言电话")
            self.socket.status = False
            exit(0)
            return

        # 来电
        if data["type"] == "call" and data["from"] != self.id:
            print(self.list[data["from"]]["nickname"] + "来电")
            play = audio.Audio()
            if play.new():
                self.ws_client.send('{"type": "answer","toId": ' + str(data["from"]) + '}')  # 回复确认接听
                self.socket = udp.Udp(play)
                self.socket.login(str(data["from"]), self.token)
                print("已自动接听来电")
            else:
                time.sleep(1)
                print("已自动拒绝来电")
                self.ws_client.send('{"type": "refuse","toId": ' + str(data["from"]) + '}')  # 回复确认接听
            return

    # 获取用户列表
    def get_list(self):
        res = self.req.get("/api/user/list")
        if res["code"] != 200:
            print(res["msg"])
            return

        online = "\n"
        for item in res["data"]["items"]:
            self.list[item["id"]] = item
            online += "[" + str(item["id"]) + "] " + item["nickname"] + " (" + str(item["username"]) + ")\n"

        print("---------------------------\n       用户列表\n---------------------------\n", online, "\n---------------------------\n")