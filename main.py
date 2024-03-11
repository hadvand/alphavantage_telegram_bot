from database.common.models import db, History
from database.core import crud

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from settings import SiteSettings
from tg_api.callbacks import router


async def main():
    site = SiteSettings()
    bot = Bot(token=site.api_token.get_secret_value())
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
