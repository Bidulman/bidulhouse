from fastapi import FastAPI, Request
import uvicorn

from data import Config, Database
from bot import Bot


class API:

    def __init__(self, config: Config, database: Database, bot: Bot):
        self.config = config
        self.database = database
        self.bot = bot
        self.app = FastAPI()
        self.load_routes()
        self.start()

    def load_routes(self):
        @self.app.post("/alerts")
        async def alerts(request: Request):
            try:
                data = await request.json()
                if data["alert"] in self.config.alerts.keys():
                    alert = self.config.alerts[data["alert"]]

                    users = self.database.get_users_with_permission(alert["permission"])
                    users_names = []
                    for user in users:
                        self.bot.send_message(user, alert["message"])
                        users_names.append(self.database.get_user(user)[1])

                    if len(users_names) > 1:
                        users_string = (" " + self.config.messages.get("and") + " ").join([", ".join(users_names[0:-1]), users_names[1]])
                    else:
                        users_string = users_names[0]

                    print("[INFO] " + self.config.messages.get("api.alerts.sent").format(alert=data["alert"], users=users_string))
                    return "Alert sent"

                print("[INFO] " + self.config.messages.get("api.alerts.received").format(alert=data["alert"]))
                return "Alert received"

            except Exception as exception:
                print(self.config.messages.get("api.alerts.error").format(error=str(exception)))

    def start(self):
        log_config = uvicorn.config.LOGGING_CONFIG
        log_config["formatters"]["default"]["fmt"] = "[%(levelname)s] %(message)s"
        log_config["formatters"]["access"]["fmt"] = "[%(levelname)s] %(message)s"
        uvicorn.run(app=self.app, host=self.config.api.host, port=self.config.api.port, log_config=log_config)
