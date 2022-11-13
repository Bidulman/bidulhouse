from json import load


class Config:
    def __init__(self, path, script):
        self.path = path
        with open(path, "r", encoding="utf-8") as file:
            self.data = load(file)

        self.api = APIConfig(self.data)
        self.mysql = MySQLConfig(self.data, script)
        self.telegram = TelegramConfig(self.data)
        self.messages = MessagesConfig(self.data)
        self.alerts = self.data["alerts"]


class APIConfig:
    def __init__(self, data):
        data = data["api"]
        self.host = data["host"]
        self.port = data["port"]


class MySQLConfig:
    def __init__(self, data, script):
        data = data["mysql"]
        self.host = data["host"]
        self.port = data["port"]
        self.database = data["database"]
        self.user = data[script]["user"]
        self.password = data[script]["password"]


class TelegramConfig:
    def __init__(self, data):
        data = data["telegram"]
        self.token = data["token"]


class MessagesConfig:
    def __init__(self, data):
        self.data = data["messages"]

    def get(self, message):
        return self.data[message]
