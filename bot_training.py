import json
import logging

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(display_name=display_name,
                               training_phrases=training_phrases,
                               messages=[message])

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    logger.info("Intent created: {}".format(response))


def list_intent_names(project_id):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    intents = intents_client.list_intents(request={"parent": parent})
    return [intent.display_name for intent in intents]


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logging.basicConfig(
        format='%(levelname)s: %(name)s - %(message)s - %(asctime)s',
        level=logging.INFO)
    logger = logging.getLogger('Logger')

    project_id = env.str('PROJECT_ID')

    with open("training_phrases.json", "r", encoding="utf-8") as file:
        training_phrases = json.load(file)

    for phrase in training_phrases:
        display_name = phrase
        if display_name not in list_intent_names(project_id):
            training_phrases_parts = training_phrases[display_name]["questions"]
            message_texts = [training_phrases[display_name]["answer"]]

            create_intent(project_id, display_name, training_phrases_parts,
                          message_texts)
        else:
            logger.error(f'Intent with name "{display_name}" already exists')
