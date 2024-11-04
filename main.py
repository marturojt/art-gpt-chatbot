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


# import the keep_alive function from the helpers module and variables from the data module
from helpers import keep_alive, search_user, new_user, chat_assistant_text, chat_assistant_photo

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
    """ Welcome bot message and manage for /start and /help commands

    Args:
        message (types.Message): The message received from the user in the chat
    """
    await message.answer("Soy ArtFinBot, tu asistente de finanzas y estare encantado de ayudarte con tus dudas sobre el uso de tu dinero y productos financieros.")

    user_db = search_user(message.from_user.id)

    if user_db:
        await message.answer("Hola de nuevo, " + user_db.name + "!")
    else:
        new_user(message.from_user.id, message.from_user.full_name)

# ChatGPT functionality
@dp.message()
async def gpt(message: types.Message):


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
        # print(response_txt)
        await message.answer(response_txt, parse_mode=ParseMode.MARKDOWN)
    elif message.content_type == ContentType.PHOTO:
        # Download the photo
        photo = message.photo[-1]
        file_info = await message.bot.get_file(photo.file_id)
        file_path = f"downloads/{photo.file_id}.jpg"
        await message.bot.download_file(file_info.file_path, destination=file_path)
        response_txt = await chat_assistant_photo(file_path, user_name, user_id)
        await message.answer(response_txt, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("Otro tipo de contenido y de momento no podemos hacer algo. Solo texto y fotos por el momento.")
        print(message.content_type)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())