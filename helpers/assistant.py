import datetime
import json
import configparser

from openai import OpenAI
from .db_interaction import get_user_thread, new_user_thread


# Import variables from config file
config = configparser.ConfigParser()
config.read("config.ini")

# Set OpenAI API key
# openai.api_key = api_options.openai_key
client = OpenAI(
    api_key=config["misc-keys"]["openai_key"]
)
model = "gpt-3.5-turbo"


# retrive assitant id from openai
my_assistant = client.beta.assistants.retrieve(config["misc-keys"]["assistant_id"])

# Create thread func
def create_thread():
    my_thread = client.beta.threads.create() # create empty thread
    return my_thread.id

# Run assistant func
def run_assistant(thread_id: str, message: str):
    my_run = client.beta.threads.runs.create(
        assistant_id=my_assistant.id,
        thread_id=thread_id,
        
        # instructions=message
    )
    return my_run

# Retrieve run status func
def retrieve_run_status(thread_id: str, run_id: str):
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    return keep_retrieving_run

# manage message func
def chat_assitant_nutribot(message: str, user_name: str, user_id: int):
    # validate if user has active thread
    user_thread = get_user_thread(user_id)

    if user_thread:
        thread_id = user_thread.thread_id
    else:
        thread_id = create_thread()
        # create new user thread (db record)
        new_user_thread(user_id, thread_id)


    # Add a Message to a Thread
    my_thread_message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )

    # run the assistant
    my_run = run_assistant(thread_id, message)

    # Loop until get any response
    while my_run.status in ["queued", "in_progress"]:
        keep_retrieving_run = retrieve_run_status(thread_id, my_run.id)

        if keep_retrieving_run.status == "completed":

            # Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )

            return all_messages.data[0].content[0].text.value

        elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
            pass
        else:
            return "Error"




