import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (CallbackContext,
                          CommandHandler,
                          Filters,
                          MessageHandler,
                          Updater)

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

LANGUAGE_CODE = "ru-RU"




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

    vk_group_token = env.str('VK_TOKEN')

    vk_session = vk_api.VkApi(token=vk_group_token)
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


    project_id = env.str('PROJECT_ID')
    session_id = env.str('SESSION_ID')







