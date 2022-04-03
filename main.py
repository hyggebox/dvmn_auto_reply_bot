import logging

from environs import Env
from telegram import Update
from telegram.ext import (CallbackContext,
                          CommandHandler,
                          Filters,
                          MessageHandler,
                          Updater)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет! Я бот")


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=update.message.text)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(levelname)s: %(name)s - %(message)s - %(asctime)s',
        level=logging.INFO)

    env = Env()
    env.read_env()

    tg_bot_token = env.str('TG_BOT_TOKEN')

    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
