import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv  # Для загрузки переменных окружения
import keyboards as kb
from aiogram import F, Router

# Загрузка переменных из файла .env
load_dotenv()

# Получаем токен бота из переменных окружения
TOKEN = os.getenv("API_TOKEN")

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем роутер для хендлеров (обработчиков сообщений и callback)
router = Router()

# Команда /start с выводом меню
@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Выберите действие:", reply_markup=kb.menu_keyboard)

# Обработка кнопки "Привет"
@router.message(F.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

# Обработка кнопки "Пока"
@router.message(F.text == "Пока")
async def say_goodbye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Команда /links для показа кнопок с ссылками
@router.message(F.text == "/links")
async def show_links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=kb.links_keyboard)

# Команда /dynamic для показа кнопки "Показать больше"
@router.message(F.text == "/dynamic")
async def show_dynamic(message: Message):
    await message.answer("Нажмите, чтобы показать больше опций:", reply_markup=kb.dynamic_keyboard)

# Обработка нажатия на кнопку "Показать больше"
@router.callback_query(F.data == "show_more")
async def show_more_options(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Выберите опцию:", reply_markup=kb.more_options_keyboard)

# Обработка опции 1
@router.callback_query(F.data == "option_1")
async def select_option_1(callback_query: CallbackQuery):
    await callback_query.answer("Вы выбрали Опцию 1")
    await callback_query.message.answer("Опция 1 выбрана")

# Обработка опции 2
@router.callback_query(F.data == "option_2")
async def select_option_2(callback_query: CallbackQuery):
    await callback_query.answer("Вы выбрали Опцию 2")
    await callback_query.message.answer("Опция 2 выбрана")

# Регистрация роутера в диспетчере
dp.include_router(router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
