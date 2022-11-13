from data import Config
from data import Database

from shell import Console

config = Config("myconfig.json", "client")
database = Database(
    config.mysql.host,
    config.mysql.port,
    config.mysql.user,
    config.mysql.password,
    config.mysql.database
)

Console(config, database)
