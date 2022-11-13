from data import Config
from data import Database
from bot import Bot
from api import API

config = Config("config.json")
database = Database(
    config.mysql.host,
    config.mysql.port,
    config.mysql.user,
    config.mysql.password,
    config.mysql.database
)

bot = Bot(config, database)

api = API(config, database, bot)
