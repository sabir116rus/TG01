import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
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


# Создаем группу состояний
class WeatherState(StatesGroup):
    waiting_for_city = State()


# Команда start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот для прогноза погоды.\nНапиши /weather, чтобы получить прогноз погоды.")


# Команда help
@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer(
        "Я могу показать прогноз погоды для заданного города. Используй команду /weather для получения информации.")


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


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
