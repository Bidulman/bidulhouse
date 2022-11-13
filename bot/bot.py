from telegram.update import Update
from telegram.parsemode import ParseMode
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler

from data import Config, Database


class Bot:

    def __init__(self, config: Config, database: Database):
        self.config = config
        self.database = database
        self.updater = Updater(config.telegram.token, use_context=True)
        self.dispatcher: Dispatcher = self.updater.dispatcher
        self.load_commands()
        self.start()

    def load_commands(self):
        def start(update: Update, context: CallbackContext):
            self.database.set_user(update.effective_user.id, update.effective_user.name)
            self.send_message(update.effective_chat.id, self.config.messages.get("command.start.out"))

        def profile(update: Update, context: CallbackContext):
            self.database.set_user(update.effective_user.id, update.effective_user.name)
            self.send_message(update.effective_chat.id, self.config.messages.get("command.profile.out").format(id=update.effective_user.id, name=update.effective_user.name))

        self.dispatcher.add_handler(CommandHandler("start", start))
        self.dispatcher.add_handler(CommandHandler("profile", profile))

    def start(self):
        print("[INFO] Starting Telegram bot...")
        self.updater.start_polling()

    def send_message(self, user, message):
        self.updater.bot.send_message(user, message, parse_mode=ParseMode.MARKDOWN)
