import requests
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from googletrans import Translator
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = Translator()

# Создание папки для хранения фотографий, если её нет
if not os.path.exists('img'):
    os.makedirs('img')

# Создаем группу состояний
class WeatherState(StatesGroup):
    waiting_for_city = State()


# Команда start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот для разных задач.\nНапиши /help, чтобы получить список команд.")


# Команда help
@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer(
        "/start - Приветствие,\n/help - Все команды бота,\n/weather - Узнать погоду в любом городе,\n/voice - Бот отправит голосовое сообщение.\nНапишите боту любой текст по русски и он переведет его в английский язык.")


# Команда для начала получения прогноза погоды
@dp.message(Command("weather"))
async def ask_city(message: types.Message, state: FSMContext):
    await message.answer("Введите название города, чтобы узнать погоду:")
    await state.set_state(WeatherState.waiting_for_city)


# Обработка ввода города от пользователя
@dp.message(WeatherState.waiting_for_city)
async def get_weather_for_city(message: types.Message, state: FSMContext):
    city = message.text
    weather_data = get_weather_data(city)
    if weather_data:
        await message.answer(f"Прогноз погоды в {city}:\n"
                             f"Температура: {weather_data['temp']}°C\n"
                             f"Ощущается как: {weather_data['feels_like']}°C\n"
                             f"Описание: {weather_data['description']}")
    else:
        await message.answer("Не удалось получить данные о погоде. Проверьте правильность названия города.")

    # Завершаем состояние
    await state.clear()


# Функция для получения данных о погоде
def get_weather_data(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            weather = {
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description']
            }
            return weather
        else:
            return None
    except requests.exceptions.Timeout:
        print("Превышено время ожидания ответа от сервера")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка: {e}")
        return None

# Функция для сохранения фото
@dp.message(F.photo)
async def handle_photos(message: types.Message):
    # Получаем файл и его уникальный идентификатор
    photo = message.photo[-1]  # берем фото с максимальным разрешением
    file_id = photo.file_id

    # Скачиваем фото
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"

    # Сохраняем фото в папке img
    response = requests.get(file_url)
    if response.status_code == 200:
        file_name = os.path.join("img", f"{file_id}.jpg")
        with open(file_name, 'wb') as f:
            f.write(response.content)
        await message.answer("Фото успешно сохранено!")
    else:
        await message.answer("Не удалось скачать фото.")

# Функция для отправки голосового сообщения
@dp.message(Command("voice"))
async def voice(message: Message):
    # Заготовленный голосовой файл
    voice = FSInputFile("voice.ogg")  # Замените "voice.ogg" на реальный файл
    await message.answer_voice(voice)

# Функция для перевода текста на английский
@dp.message(F.text)
async def translate_text(message: types.Message):
    text = message.text
    translated = translator.translate(text, dest='en')
    await message.answer(f"Перевод на английский:\n{translated.text}")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
