import asyncio
import logging

from aiogram import Bot
from aiogram.types import InputFile
from aiogram import exceptions


async def send_document(bot: Bot, user_id: int, text, document_path, protect_content: bool = False,
                        reply_markup=None) -> bool:
    try:
        await bot.send_document(user_id, document_path, caption=text, protect_content=protect_content,
                                reply_markup=reply_markup)
    except (exceptions.BotBlocked, exceptions.ChatNotFound, exceptions.UserDeactivated):
        logging.exception(f"Error:")
        return False
    
    except exceptions.TelegramRetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        
        await asyncio.sleep(e.retry_after)
        return await send_document(bot, user_id, text, document_path, protect_content, reply_markup)  # Recursive call
    
    except exceptions.TelegramAPIError:
        logging.exception(f"Error:")
        return False
    
    except:
        logging.exception(f"Error у пользователя {user_id}:")


async def send_message(bot: Bot, user_id: int, text: str, media=None, kb=None) -> bool:
    try:
        if media:
            media_keys = media.keys()
            if "0" in media_keys:
                await bot.send_audio(chat_id=user_id, audio=media.get("0"), caption=text)
            elif '1' in media_keys:
                await bot.send_video(chat_id=user_id, video=media.get("1"), caption=text)
            elif '2' in media_keys:
                await bot.send_document(chat_id=user_id, document=media.get("2"), caption=text)
            elif '3' in media_keys:
                await bot.send_photo(chat_id=user_id, photo=media.get("3"), caption=text)
            else:
                return False
        else:
            await bot.send_message(chat_id=user_id, text=text, disable_web_page_preview=True, reply_markup=kb)
    except (exceptions.TelegramBadRequest):
        return False
    
    except exceptions.TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_message(bot, user_id, text, media, kb)  # Recursive call
    
    except exceptions.TelegramAPIError:
        pass
    else:
        return True
    
    return False
