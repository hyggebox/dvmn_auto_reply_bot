import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (CallbackContext,
                          CommandHandler,
                          Filters,
                          MessageHandler,
                          Updater)


LANGUAGE_CODE = "ru-RU"


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет! Я бот")


def echo(update: Update, context: CallbackContext):
    user_msg = update.message.text
    bots_answer = detect_intent_texts(project_id, session_id,
                                      user_msg, LANGUAGE_CODE)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=bots_answer)


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


if __name__ == '__main__':
    logging.basicConfig(
        format='%(levelname)s: %(name)s - %(message)s - %(asctime)s',
        level=logging.INFO)

    env = Env()
    env.read_env()

    tg_bot_token = env.str('TG_BOT_TOKEN')
    project_id = env.str('PROJECT_ID')
    session_id = env.str('SESSION_ID')

    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
