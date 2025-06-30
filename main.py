import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from tgbot.database.db import db
from tgbot.misc.check_server import Webhook
from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.handlers.admin.menu import register_admin
from tgbot.handlers.user.user import register_user
from bot import logger, config, scheduler


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)

    

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    
    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=storage)
    
    register_all_handlers(dp)
    await set_default_commands(dp, config.tg_bot.admin_ids)
    
    # start
    try:
        scheduler.start()
        await dp.start_polling(bot, skip_updates=False)
    finally:
        await dp.storage.close()
        session = bot.session

        if session:
            await session.close()
        


if __name__ == '__main__':
    try:
        aiogram_loop = asyncio.get_event_loop()
        aiogram_loop.create_task(Webhook.reader(db, scheduler))
        aiogram_loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")