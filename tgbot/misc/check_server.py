import asyncio
import json
import logging
from datetime import datetime, timedelta

import aioredis
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config
from tgbot.keyboards.inline import demo_link_kb
from tgbot.misc.broadcast import send_document, send_message


async def message_with_24_hour_delay(user_id):
    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    await send_message(bot, user_id, """
<b>Всё ли открылось, скачалось, возможно даже удалось прочитать?
</b> Надеюсь, чек-лист дал вам ясность, хотя бы в одном важном моменте❤️ Иногда вовремя сказанная фраза, как фонарик подсвечивает риски.

Но если хочется не просто выходить из неправильного, а входить в правильное шаг за шагом, посмотрите демоверсию курса <b>«ДА!НО:»</b>.

<b>Это практикум</b>. Про то, как строить отношения от первого сообщения до <i>«жили они долго и счастливо».</i> Что говорить, как сближаться, когда ждать, а когда звать. Как делать всё в нужный момент, чтобы строить счастливые отношения
""", kb=demo_link_kb())

    session = bot.session
    if session:
        await session.close()


class Webhook:
    bot = None
    db = None

    @classmethod
    async def handle_payment_callback(cls, data):
        user_id = data.get('Unpauseme_user_id')
        if user_id is not None:
            cls.db.update_date_of_purchase(user_id, (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"))
            await send_document(cls.bot, user_id, text="""
❤️ Спасибо за доверие.
Вы сделали важный шаг - в сторону ясности, достоинства и настоящих отношений.
⠀
Внимательно прочтите чек-лист. Отметьте фразы, которые слышали и вспомните свои реакции.
⠀
<b>Выбирайте быть воздухом, а не пластырем. И пусть рядом окажется тот, кто ищет не утешение, а встречи.</b>
⠀
Если будут вопросы - возвращайтесь. 
<i>(Я рядом, в каждом комментарии канала А что, если Да?)
</i>
""",
                                document_path="BQACAgIAAxkBAAMnaGHwJAABLBlcUK89skBpfskV4R1gAAIFcwAC4IgQSxKLlRhqSZY_NgQ")

        scheduler: AsyncIOScheduler = cls.bot['scheduler']
        date = datetime.now()
        hours_24 = date + timedelta(hours=24)

        scheduler.add_job(message_with_24_hour_delay, 'date', run_date=hours_24, args=(user_id,))

    @classmethod
    async def reader(cls, db, scheduler):
        cls.db = db
        config = load_config(".env")
        cls.bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
        cls.bot['scheduler'] = scheduler

        redis = aioredis.from_url("redis://localhost", db=4)
        channel = "Unpauseme_payment_channel"

        while True:
            try:
                # Ожидаем сообщения из Redis канала
                message = await redis.lpop(channel)
                if message is None:
                    await asyncio.sleep(10)
                    continue

                data = json.loads(message)
                await cls.handle_payment_callback(data)

            except asyncio.TimeoutError:
                pass
            except:
                logging.exception('Error:')
            await asyncio.sleep(10)
