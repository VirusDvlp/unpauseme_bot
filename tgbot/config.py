from dataclasses import dataclass

import os
from typing import List

from dotenv import load_dotenv


load_dotenv()

@dataclass
class TgBot:
    token: str
    admin_ids: List[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=os.getenv("BOT_TOKEN"),
            admin_ids=list(map(int, os.getenv("ADMINS").split(',')))
        )
    )
