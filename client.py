from data import Config
from data import Database

from shell import Console

config = Config("config.json", "client")
database = Database(
    config.mysql.host,
    config.mysql.port,
    config.mysql.user,
    config.mysql.password,
    config.mysql.database
)

Console(config, database)
