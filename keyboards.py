from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Меню с кнопками "Привет" и "Пока"
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True
)

# Кнопки с URL-ссылками
links_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url='https://www.forbes.ru/mneniya/507469-programmistom-budet-kazdyj-cto-zdet-razrabotcikov-v-epohu-nejrosetej')],
        [InlineKeyboardButton(text="Музыка", url='https://music.yandex.ru/album/21940/track/178529')],
        [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/watch?v=NXpdyAWLDas')]
    ]
)

# Кнопка "Показать больше"
dynamic_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ]
)

# Новые кнопки "Опция 1" и "Опция 2"
more_options_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ]
)
