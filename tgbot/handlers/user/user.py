import asyncio
from datetime import datetime, timedelta

from aiogram import Dispatcher, types, Bot
from aiogram.filters import CommandStart, StateFilter

from apscheduler.triggers.date import DateTrigger

from tgbot.database.db import db
from tgbot.keyboards.inline import payment_kb
from tgbot.misc.broadcast import send_message
from tgbot.misc.utils import get_payment_link
from bot import scheduler, config


async def user_start(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    text = """
<b>Иногда всё начинается с </b><b><i>«не как у всех». 
</i></b>
Он тонко чувствует. Говорит <i>«с тобой так легко», «ты мой воздух», «я сам не знаю, что делать...»</i>

И вы — вроде взрослая, с опытом, знаете, чего хотите... и всё равно ловите себя на мысли: <b><i>«А вдруг?..»
</i></b>
Но есть тонкая грань между настоящим началом и тем, что называется временной ролью.
Не нужно быть психологом или детективом, чтобы распознать это вовремя.
Я собрала <b>чек-лист, который поможет сохранить себя и не спутать желание быть любимой с чужим удобством</b>

👇
"""
    await message.answer(text)
    await asyncio.sleep(20)
    url = get_payment_link(message.from_user.id)

    await message.answer_photo('AgACAgIAAxkBAAMEaGC-HN44it03ASjzrN-2c1NxYEAAAmv1MRtE1AlLUPNVe9yIT5UBAAMCAANzAAM2BA', caption="""
<b>Хотите отношений, но снова натыкаетесь на женатых, ветреных или </b><b><i>«ещё не готов»</i>?
</b>
Я собрала для вас <b>чек-лист «Как не стать временной»</b> - это честная инструкция-оберег.

Она поможет вовремя различить: перед вами мужчина счастливого будущего или вы застряли между его <i>«ещё»</i> и <i>«пока».</i>
⠀
Простые фразы, чёткие признаки и слова, с которыми вы сможете уйти с достоинством, если поймёте, что играете не свою роль.
⠀
<b>Забирайте Чек-лист</b> и не позволяйте себе быть чьей-то паузой🙌
⠀
(<i>Сейчас со скидкой 50% — только для подписчиц канала)</i>
""", reply_markup=payment_kb(url))
    date = datetime.now()
    minute_30 = date + timedelta(minutes=30)

    scheduler.add_job(message_with_30_minute_delay, DateTrigger(run_date=minute_30), args=(message.from_user.id,))


async def message_with_30_minute_delay(user_id):
    user = db.get_user(telegram_id=user_id)

    if user[3]:
        return
    url = get_payment_link(user_id)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    await send_message(bot, user_id, """
Иногда в последний момент что-то отвлекает и важные решения откладываются. 
<b>Чек-лист «Как не стать временной»</b> поможет избежать лишних поворотов и сберечь ваше время. Если сейчас это для вас актуально — он всё ещё здесь
👇
""",
                       kb=payment_kb(url))
    date = datetime.now()
    hours_24 = date + timedelta(hours=24)

    scheduler.add_job(message_with_24_hours_delay, DateTrigger(run_date=hours_24), args=(user_id,))

    session = bot.session
    if session:
        await session.close()


async def message_with_24_hours_delay(user_id):
    user = db.get_user(telegram_id=user_id)

    if user[3]:
        return
    url = get_payment_link(user_id)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    await send_message(bot, user_id, """
Спасибо, что заглянули. Я очень ценю ваше внимание и не буду больше тревожить❤️ ⠀ Но если почувствуете, что хочется ясности и честных ориентиров в отношениях — знайте, чек-лист <b>«Как не стать временной»</b> всегда доступен. ⠀ Оставайтесь в канале «А что, если Да?». 
В ближайшее время там будет очень много полезного👌
""",
                       kb=payment_kb(url))

    session = bot.session
    if session:
        await session.close()



def register_user(dp: Dispatcher):
    dp.message.register(user_start, CommandStart(), StateFilter('*'))
