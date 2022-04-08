import logging

from environs import Env
from telegram import Bot, Update
from telegram.ext import (CallbackContext,
                          CommandHandler,
                          Filters,
                          MessageHandler,
                          Updater)
from time import sleep

from df_msg_handler import get_reply_msg


logger = logging.getLogger("Logger")


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет! Я бот")


def send_reply_msg(update: Update, context: CallbackContext):
    user_msg = update.message.text
    bots_answer = get_reply_msg(project_id, session_id, user_msg)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=bots_answer)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    tg_bot_token = env.str('TG_BOT_TOKEN')
    project_id = env.str('PROJECT_ID')
    session_id = env.str('SESSION_ID')
    tg_admin_chat_id = env.str('TG_ADMIN_CHAT_ID')

    bot = Bot(token=tg_bot_token)
    logger.setLevel(level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, tg_admin_chat_id))
    logger.info("Бот запущен")

    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command),
                                  send_reply_msg)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    while True:
        try:
            updater.start_polling()
        except Exception as err:
            logger.exception(f"⚠ Ошибка бота:\n\n {err}")
            sleep(60)
