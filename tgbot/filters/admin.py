import typing

from aiogram.filters import BaseFilter

from bot import config


class AdminFilter(BaseFilter):

    async def __call__(self, obj):
        return obj.from_user.id in config.tg_bot.admin_ids

