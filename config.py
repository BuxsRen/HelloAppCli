import configparser


# 加载配置文件
class Config:
    cfp = None

    def __init__(self, path='app.ini'):
        self.cfp = configparser.ConfigParser()
        self.cfp.read(path)

    def get_config(self, option, key):
        if self.cfp.has_section(option):
            return self.cfp.get(option, key)
        else:
            return ""


Conf = Config()

