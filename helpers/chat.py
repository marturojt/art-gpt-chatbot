import datetime
import json
import configparser

from openai import OpenAI
from .db_interaction import get_asistant_role_by_id, get_chat_log_user, new_chat_log_entry


# Import variables from config file
config = configparser.ConfigParser()
config.read("config.ini")

# Set OpenAI API key
# openai.api_key = api_options.openai_key
client = OpenAI(
    api_key=config["misc-keys"]["openai_key"]
)
model = "gpt-3.5-turbo"

# Dictionary to store conversation state
conversation_state = {}


def chat_openai_nutribot(message: str, user_name: str, user_id: int):

    # Get the assitant role
    role_db = get_asistant_role_by_id(1)
    system_role = f"{role_db.AsistantRole}".replace(
        "XXXUSUARIOXXX", user_name).replace("XXXASISTENTEXXX", "Nutribot")

    # Create the initial message with the system prompt
    messages = [{"role": "system", "content": system_role},]

    chat_log = get_chat_log_user(user_id)
    if chat_log:
        for log in chat_log:
            # print(log[0])
            json_dict = json.loads(log[0])
            messages.append(json_dict)
        # messages.append(chat_log)

    # Append message
    new_message = {"role": "user", "content": message}
    messages.append(new_message)

    # print(messages)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        # max_tokens=300,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0
    )
    text_user = json.dumps(new_message)
    new_chat_log_entry(user_id, text_user, datetime.datetime.now())
    text_response = json.dumps({"role": "assistant", "content": response.choices[0].message.content})
    new_chat_log_entry(user_id, text_response, datetime.datetime.now())

    return response.choices[0].message.content
