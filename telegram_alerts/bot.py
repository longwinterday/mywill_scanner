from telegram.ext import Updater, CommandHandler

from settings import CONFIG
from .storage import get_saved_chat_ids, write_new_chat_ids

help_message = """/help - see command and description again\n
/ping - Check if I'm alive\n
/register - you subscibing into my spam hell\n
/stop - i will stop send you all this logs\n
"""


def start(update, context):
    text = ("Hi! I'm alert bot for one of scanner projects\n"
            "I have several commands, like:\n\n"
            + help_message +
            "With these commands you can start me here "
            "or inside a chat with your friends.\n"
            "You can all enjoy my bug reports! "
            )
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def bot_help(update, context):
    text = help_message
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def ping(update, context):
    text = "I'm alive, scanner working now, muddy is mudding, laveha is spinning"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def register(update, context):
    chat_id = update.effective_chat.id
    lines = get_saved_chat_ids()
    if chat_id not in get_saved_chat_ids():
        lines.append(chat_id)
        write_new_chat_ids(lines)
        text = "You subscribed on errors, spam will start soon"
    else:
        text = 'What do you want?! You already subscribed!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def stop(update, context):
    chat_id = update.effective_chat.id
    lines = get_saved_chat_ids()
    if chat_id in lines:
        lines.remove(chat_id)
        write_new_chat_ids(lines)
        text = "You unsubscribed on errors, feel free.. for now 😈"
    else:
        text = 'You do not even subscribed! Fukoff!'

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


class AlertBot:
    def __init__(self):
        token = CONFIG.get('telegram_token')
        if not token:
            self.updater = None
            print('WARNING! Cant start bot without token in settings', flush=True)
            return

        self.updater = Updater(token=token, use_context=True)
        dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', start)
        help_handler = CommandHandler('help', bot_help)
        ping_handler = CommandHandler('ping', ping)
        register_handler = CommandHandler('register', register)
        stop_handler = CommandHandler('stop', stop)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(help_handler)
        dispatcher.add_handler(ping_handler)
        dispatcher.add_handler(register_handler)
        dispatcher.add_handler(stop_handler)

    def start_polling(self):
        if not self.updater:
            return

        self.updater.start_polling()

    def send_messages(self, text):
        if not self.updater:
            return

        ids = get_saved_chat_ids()
        for _id in ids:
            self.updater.bot.send_message(_id, text)


alert_bot = AlertBot()
