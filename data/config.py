from json import load


class Config:
    def __init__(self, path):
        self.path = path
        with open(path, "r", encoding="utf-8") as file:
            self.data = load(file)

        self.api = APIConfig(self.data)
        self.mysql = MySQLConfig(self.data)
        self.telegram = TelegramConfig(self.data)
        self.messages = MessagesConfig(self.data)
        self.alerts = self.data["alerts"]


class APIConfig:
    def __init__(self, data):
        data = data["api"]
        self.host = data["host"]
        self.port = data["port"]


class MySQLConfig:
    def __init__(self, data):
        data = data["mysql"]
        self.host = data["host"]
        self.port = data["port"]
        self.user = data["user"]
        self.password = data["password"]
        self.database = data["database"]


class TelegramConfig:
    def __init__(self, data):
        data = data["telegram"]
        self.token = data["token"]


class MessagesConfig:
    def __init__(self, data):
        self.data = data["messages"]

    def get(self, message):
        return self.data[message]
