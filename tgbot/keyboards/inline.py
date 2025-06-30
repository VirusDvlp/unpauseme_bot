from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_kb(url):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Да-Да! КУПИТЬ чек-лист 🙌', url=url)]
        ]
    )


def demo_link_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Посмотреть демоверсию курса🔥', url='https://t.me/+bcT53l5ZkyE2MzNi')]
        ]
    )
