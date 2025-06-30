import csv

from aiogram import types, Dispatcher, F
from aiogram.filters import Command

from tgbot.database.db import db
from tgbot.filters.admin import AdminFilter


async def get_data_csv(message: types.Message):

    users = db.select_users()
    with open('tgbot/files/data.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Запись заголовков (необязательно)
        writer.writerow(['telegram_id', 'Имя', 'Username', "Дата оплаты"])

        # Запись данных
        for row in users:
            writer.writerow(row)
    await message.answer_document(types.InputFile('tgbot/files/data.csv'))


def register_admin(dp: Dispatcher):
    dp.message.register(get_data_csv, Command('data'), AdminFilter())
