
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()
config = load_config()

