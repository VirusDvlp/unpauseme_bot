from aiogram import types, Dispatcher, Bot


async def set_default_commands(bot: Bot, admin_id):
    try:
        await bot.set_my_commands(
            [
                types.BotCommand("data", "Выгрузить csv"),
            ],
            scope=types.BotCommandScopeChat(admin_id)
        )
    except:
        pass
