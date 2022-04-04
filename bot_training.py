import json

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)

        # Here we create a new training phrase for each provided part.
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

    print("Intent created: {}".format(response))


if __name__ == "__main__":
    env = Env()
    env.read_env()

    project_id = env.str('PROJECT_ID')

    with open("training_phrases.json", "r", encoding="utf-8") as file:
        training_phrases = json.load(file)

    display_name = "Устройство на работу"
    training_phrases_parts = training_phrases[display_name]["questions"]
    message_texts = training_phrases[display_name]["answer"]

    create_intent(project_id, display_name, training_phrases_parts,
                  message_texts)
