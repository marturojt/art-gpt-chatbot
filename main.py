import asyncio
import logging
import sys
import configparser
from os import getenv

from aiogram import Bot, Dispatcher, html, types, md
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, BotCommand, ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown as md

from pdf2image import convert_from_path

# import the keep_alive function from the helpers module and variables from the data module
from helpers import keep_alive, search_user, new_user, chat_assistant_text, chat_assistant_photos

# Import variables from config file
config = configparser.ConfigParser()
config.read("config.ini")

# flask server to test if the bot is alive
keep_alive()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = config["misc-keys"]["telegram_key"]

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# Command handlers for /start and /help
@dp.message(Command(BotCommand(command="start", description="Start the bot and show welcome message")))
@dp.message(Command(BotCommand(command="help", description="Show help message")))
async def command_start_handler(message: Message) -> None:
    """
    Handles the /start command for the bot.
    This function is triggered when a user sends the /start command. It sends a welcome message to the user and checks if the user exists in the database. If the user exists, it sends a personalized greeting. If the user does not exist, it creates a new user entry in the database.
    Args:
        message (Message): The message object containing information about the user and the message sent.
    Returns:
        None
    """
    await message.answer(config["messages"]["welcome_message"])

    user_db = search_user(message.from_user.id)

    if user_db:
        await message.answer("Hola de nuevo, " + user_db.name + "!")
    else:
        new_user(message.from_user.id, message.from_user.full_name)

# ChatGPT functionality
@dp.message()
async def gpt(message: types.Message):
    """
    Handles incoming messages and processes them based on their content type.
    Args:
        message (types.Message): The incoming message object from the user.
    The function performs the following steps:
    1. Retrieves the user from the database using their ID. If the user does not exist, it creates a new user.
    2. Validates the content type of the message and processes it accordingly:
        - If the message contains text, it calls `chat_assistant_text` to generate a response.
        - If the message contains a photo, it calls `handle_photo` to process the photo.
        - If the message contains a document, it calls `handle_document` to process the document.
        - For other content types, it sends a default response indicating unsupported content.
    The function sends the generated response back to the user using the appropriate parse mode.
    """

    # Get user name and id
    user_db = search_user(message.from_user.id)
    if user_db is None:
        new_user(message.from_user.id, message.from_user.full_name)
        user_name, user_id = message.from_user.full_name, message.from_user.id
    else:
        user_name, user_id = user_db.name, user_db.idUser

    # validate message content type
    if message.content_type == ContentType.TEXT:
        response_txt = await chat_assistant_text(message.text, user_name, user_id)
        await message.answer(response_txt, parse_mode=ParseMode.MARKDOWN)
    elif message.content_type == ContentType.PHOTO:
        response_txt = await handle_photo(message, user_name, user_id)
        await message.answer(response_txt, parse_mode=ParseMode.MARKDOWN)
    elif message.content_type == ContentType.DOCUMENT:
        response_txt = await handle_document(message, user_name, user_id)
        await message.answer(response_txt, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("Otro tipo de contenido y de momento no podemos hacer algo. Solo texto y fotos por el momento.")
        print(message.content_type)

# Handle photo messages
async def handle_photo(message: types.Message, user_name: str, user_id: int) -> str:
    """
    Handles the photo message sent by the user.

    Args:
        message (types.Message): The message object containing the photo.
        user_name (str): The name of the user sending the photo.
        user_id (int): The ID of the user sending the photo.

    Returns:
        str: The response text generated after processing the photo.

    Raises:
        Exception: If there is an error processing the photo.
    """

    try:
        photo = message.photo[-1]
        file_info = await message.bot.get_file(photo.file_id)
        file_path = f"downloads/{photo.file_id}.jpg"
        await message.bot.download_file(file_info.file_path, destination=file_path)
        response_txt = await chat_assistant_photos([file_path], user_name, user_id)
        return response_txt
    except Exception as e:
        print(f"Error processing photo: {e}")
        return "Error processing photo"

# Handle document messages
async def handle_document(message: types.Message, user_name: str, user_id: int) -> str:
    """
    Handles the document sent by the user, processes it if it's a PDF, and returns a response.
    Args:
        message (types.Message): The message object containing the document.
        user_name (str): The name of the user who sent the document.
        user_id (int): The ID of the user who sent the document.
    Returns:
        str: A response message after processing the document.
    Raises:
        Exception: If there is an error processing the document.
    """

    try:
        document = message.document
        file_info = await message.bot.get_file(document.file_id)
        file_extension = document.file_name.split(".")[-1]
        
        if file_extension == "pdf":
            print("Downloading PDF")
            file_path = f"downloads/{document.file_id}.{file_extension}"
            await message.bot.download_file(file_info.file_path, destination=file_path)
            
            # Convert PDF to images
            images = convert_from_path(file_path)
            if len(images) > 5:
                return "El documento tiene más de 5 páginas. Solo se aceptan documentos con 5 páginas o menos."
            
            image_paths = []
            for i, image in enumerate(images):
                image_path = f"downloads/{document.file_id}_page_{i + 1}.jpg"
                image.save(image_path, 'JPEG')
                image_paths.append(image_path)
            
            # Process each image with chat_assistant_photos
            response_txt = await chat_assistant_photos(image_paths, user_name, user_id)
            return response_txt
        else:
            print("File type not supported")
            return "Lo siento, solo puedo leer archivos PDF por ahora."
    except Exception as e:
        print(f"Error processing document: {e}")
        return "Error processing document"

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())