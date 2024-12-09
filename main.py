import asyncio
import logging
import sys
import configparser
from os import getenv

from aiogram import Bot, Dispatcher, html, types, md, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, BotCommand, ContentType, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown as md
# from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from pdf2image import convert_from_path

# import the keep_alive function from the helpers module and variables from the data module
from helpers import keep_alive, search_user, new_user, chat_assistant_text, chat_assistant_photos, chat_with_func

# Import variables from config file
config = configparser.ConfigParser()
config.read("config.ini")

# flask server to test if the bot is alive
keep_alive()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = config["misc-keys"]["telegram_key"]

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
bot = Bot(token=TOKEN, parse_mode="MarkdownV2")

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
        await message.answer("Hola de nuevo, " + user_db.name )
    else:
        new_user(message.from_user.id, message.from_user.full_name)

# Command handler for /infoTDC
@dp.message(Command(BotCommand(command="infotdc", description="Show information about credit cards")))
async def command_infoTDC_handler(message: Message) -> None:
    # Crear botones inline con callbacks
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Más información 📖", callback_data="more_info_tdc")],
        [InlineKeyboardButton(text="La quiero! 🎉", callback_data="i_want_tdc")],
        [InlineKeyboardButton(text="No, gracias. 🙏", callback_data="no_thanks_tdc")]
    ])
    photo_url = "https://www.hsbc.com.mx/content/dam/hsbc/mx/images/tarjetas/advance-platinum/advance-platinum.jpg"
    caption_text = (
        "🌟 ¡Impulsa tus finanzas con una *Tarjeta de Crédito HSBC*\\! \n Descubre los beneficios que HSBC tiene para ti:\n\n"
        "\\- 💳 *HSBC Zero*: Sin comisión por administración de tarjeta del titular\\.\n"
        "\\- 💳 *HSBC 2Now*: 2% de cashback en todas tus compras al instante\\.\n"
        "\\- 💳 *HSBC VIVA*: Beneficios exclusivos para tus viajes\\."
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption= caption_text,
        reply_markup=keyboard
    )
    # await message.answer("🌟 ¡Impulsa tus finanzas con una *Tarjeta de Crédito HSBC*! \n Descubre los beneficios que HSBC tiene para ti:", reply_markup=keyboard)
    # await message.answer("Quieres una TDC, dame tu nombre completo y fecha de nacimeiento")

# Command handler for /infoLOAN
@dp.message(Command(BotCommand(command="infoloan", description="Show information about personal loans")))
async def command_infoTDC_handler(message: Message) -> None:
    await message.answer("Quieres un crédito personal, dame tu nombre completo y fecha de nacimeiento")

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
        # response_txt = await chat_assistant_text(message.text, user_name, user_id)
        response_txt = await chat_with_func(message.text, user_name, user_id)
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

# Manage callback queries from buttons
@dp.callback_query()
async def handle_callback_query(callback_query: types.CallbackQuery):
    data = callback_query.data  # Datos del callback

    if data == "more_info_tdc":
        message_text = (
            "💡 *Tarjetas de Crédito HSBC* ofrecen:\n\n"
            "- *HSBC Zero*: Sin comisión por administración de tarjeta del titular. ([Más información](https://www.hsbc.com.mx/tarjetas-de-credito/productos/zero/)) \n"
            "- *HSBC 2Now*: 2% de cashback en todas tus compras al instante. ([Más información](https://www.hsbc.com.mx/tarjetas-de-credito/productos/2now/)) \n"
            "- *HSBC VIVA*: Beneficios exclusivos para tus viajes. ([Más información](https://www.hsbc.com.mx/tarjetas-de-credito/productos/)) \n\n"

            "¿Te gustaría solicitar alguna de estas tarjetas?\n"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="La quiero! 🎉", callback_data="i_want_tdc")],
            [InlineKeyboardButton(text="No, gracias. 🙏", callback_data="no_thanks_tdc")]
        ])
        await callback_query.message.answer(message_text, reply_markup=keyboard, parse_mode="Markdown")


    elif data == "i_want_tdc":
        message_text = (
            "🎉 **¡Excelente elección!**  \n"
            "Para solicitar tu Tarjeta de Crédito HSBC:  \n\n"
            "- **En línea**: [Solicita tu tarjeta aquí](https://testflight.apple.com/v1/invite/b166c99e49d74adfaf13b0217d94e0fbc13f4dcd7bc14e15a377ed45b908d9fa18d9715bf?ct=L7UPZ62548&advp=10000&platform=ios). \n"
            "- **Sucursal**: Visita la sucursal HSBC más cercana. \n"

            "¿Necesitas asistencia adicional?"
        )
        await callback_query.message.answer(message_text, parse_mode="Markdown")
    elif data == "no_thanks_tdc":
        message_text = (
            "😌 **¡Entendido!** \n"
            "Si en el futuro deseas conocer más sobre nuestros productos, no dudes en contactarnos.  \n"
            "¿Te gustaría explorar otros servicios de HSBC? Cuentame que necesitas."
        )
        await callback_query.message.answer(message_text, parse_mode="Markdown")
    else:
        await callback_query.message.answer("Opción no reconocida.")
    
    # Confirmar que se procesó el callback para eliminar el círculo de espera en la UI
    await callback_query.answer()

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())