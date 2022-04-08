import logging
import random
import vk_api as vk

from environs import Env
from time import sleep
from vk_api.longpoll import VkLongPoll, VkEventType

from df_msg_handler import get_reply_msg


logger = logging.getLogger("Logger")


class VKLogsHandler(logging.Handler):

    def __init__(self, user_id, vk_api):
        super().__init__()
        self.user_id = user_id
        self.vk_api = vk_api

    def emit(self, record):
        log_entry = self.format(record)
        self.vk_api.messages.send(user_id=self.user_id,
                                  message=log_entry,
                                  random_id=random.randint(1,1000))


def send_reply_msg(event, vk_api, project_id, session_id):
    bots_answer = get_reply_msg(project_id, session_id, event.text)
    if bots_answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=bots_answer,
            random_id=random.randint(1,1000)
        )


if __name__ == '__main__':
    env = Env()
    env.read_env()

    vk_group_token = env.str('VK_TOKEN')
    project_id = env.str('PROJECT_ID')
    session_id = env.str('SESSION_ID')
    vk_admin_user_id = env.str('VK_ADMIN_USER_ID')

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.setLevel(level=logging.INFO)
    logger.addHandler(VKLogsHandler(vk_admin_user_id, vk_api))
    logger.info("Бот запущен")

    while True:
        try:
            for event in longpoll.listen():

                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    send_reply_msg(event, vk_api, project_id, session_id)

        except Exception as err:
            logger.exception(f"⚠ Ошибка бота:\n\n {err}")
            sleep(60)
