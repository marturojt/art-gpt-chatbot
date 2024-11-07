import datetime
import json
import configparser
import base64
import io
import os
import uuid
from PIL import Image
from openai import OpenAI
from aiogram.types import Message, BotCommand, ContentType
from .db_interaction import get_user_thread, new_user_thread


# Import variables from config file
config = configparser.ConfigParser()
config.read("config.ini")

# Set OpenAI API key
client = OpenAI(
    api_key=config["misc-keys"]["openai_key"]
)

# retrive assitant id from openai
my_assistant = client.beta.assistants.retrieve(
    config["misc-keys"]["assistant_id"])

# Create thread func
def create_thread():
    my_thread = client.beta.threads.create()  # create empty thread
    return my_thread.id

# Run assistant func
def run_assistant(thread_id: str):
    """
    Runs the assistant for a given thread.
    Args:
        thread_id (str): The ID of the thread to run the assistant on.
    Returns:
        my_run: The result of the assistant run.
    """

    my_run = client.beta.threads.runs.create(
        assistant_id=my_assistant.id,
        thread_id=thread_id,

        # instructions=message
    )
    return my_run

# Retrieve run status func
def retrieve_run_status(thread_id: str, run_id: str):
    """
    Retrieve the status of a specific run within a thread.

    Args:
        thread_id (str): The ID of the thread.
        run_id (str): The ID of the run.

    Returns:
        dict: The status information of the specified run.
    """
    
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    return keep_retrieving_run

# Chat assistant text func
async def chat_assistant_text(message: str, user_name: str, user_id: int):
    """
    Asynchronously handles a chat message from a user, processes it through an assistant, and retrieves the assistant's response.
    Args:
        message (str): The message text from the user.
        user_name (str): The name of the user.
        user_id (int): The unique identifier of the user.
    Returns:
        str: The response text from the assistant.
    Raises:
        Exception: If there is an error during the processing of the message or retrieving the assistant's response.
    """

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
    my_run = run_assistant(thread_id)

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

# Chat assistant photo func
async def chat_assistant_photos(photos: list, user_name: str, user_id: int) -> str:
    """
    Processes a list of photos, optimizes them, uploads them to a file service, 
    and interacts with a chat assistant to provide information about the images.
    Args:
        photos (list): A list of file paths to the photos to be processed.
        user_name (str): The name of the user.
        user_id (int): The ID of the user.
    Returns:
        str: The response from the chat assistant, or an error message if something goes wrong.
    Raises:
        Exception: If there is an error during the processing of photos.
    """

    # validate if user has active thread
    user_thread = get_user_thread(user_id)
    if user_thread:
        thread_id = user_thread.thread_id
    else:
        thread_id = create_thread()
        # create new user thread (db record)
        new_user_thread(user_id, thread_id)

    try:
        optimized_image_paths = []
        for photo in photos:
            # Optimize the image
            optimized_image_path = await optimize_image(photo)
            optimized_image_paths.append(optimized_image_path)

        uploaded_files = []
        for optimized_image_path in optimized_image_paths:
            # Upload the optimized image file to files api
            with open(optimized_image_path, "rb") as image_file:
                my_file = client.files.create(
                    file=image_file,
                    purpose="vision"
                )
                uploaded_files.append(my_file.id)

        # Create the message content with the uploaded images
        message_content = [
            {
                "type": "text",
                "text": "Toma información de las imágenes y continua relacionado la conversación que hemos tenido y las funciones para las que estas hecho. De ser posible, por favor, proporciona información sobre el contenido de las imágenes. Continua la conversación el idioma en el que se ha dado en los ultimos mensajes."
            }
        ]

        for file_id in uploaded_files:
            message_content.append({
                "type": "image_file",
                "image_file": {"file_id": file_id}
            })

        # Add a Message to a Thread with the optimized images
        my_thread_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_content
        )

        # Run the assistant
        my_run = run_assistant(thread_id)

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

    except Exception as e:
        print(f"Error processing photos: {e}")
        return "Error processing photos"

# Optimize image func
async def optimize_image(photo_path: str) -> str:
    """
    Optimize an image by resizing it while maintaining its aspect ratio and saving it in JPEG format with optimization.
    Args:
        photo_path (str): The file path of the image to be optimized.
    Returns:
        str: The file path of the optimized image. If optimization fails, returns the original image path.
    Raises:
        Exception: If there is an error during the image optimization process.
    """

    try:
        # Open the image file
        img = Image.open(photo_path)
        img = img.convert("RGB")  # Ensure the image is in RGB mode

        # Resize the image while maintaining aspect ratio
        max_dimension = 512  # Set your desired maximum dimension
        width, height = img.size
        if width > max_dimension or height > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            img = img.resize((new_width, new_height))

        # Save the optimized image to a new file
        optimized_image_path = f"downloads/optimized_{os.path.basename(photo_path)}"
        img.save(optimized_image_path, "JPEG", optimize=True, quality=85)

        return optimized_image_path

    except Exception as e:
        print(f"Error optimizing image: {e}")
        return photo_path  # Return the original image if optimization fails