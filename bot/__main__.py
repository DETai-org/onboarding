"""DETai Telegram welcome-only bot; no own contact database or advertising."""
import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message

from .runtime_contacts import observe_start
from .welcome import welcome_copy, welcome_keyboard

BOT_ID = "detai-onboarding"
EXPECTED_USERNAME = "detonboardingbot"
TOKEN_ENV = "DETAI_ONBOARDING_BOT_TOKEN"
WELCOME_IMAGE = Path(__file__).resolve().parent / "assets" / "welcome.png"


async def run() -> None:
    token = os.getenv(TOKEN_ENV, "").strip()
    if not token or not os.getenv("ECOSYSTEM_NOTIFICATIONS_TOKEN") or not os.getenv("ECOSYSTEM_NOTIFICATIONS_URL"):
        logging.error("Bot token and sender-scoped Runtime credentials are required")
        raise SystemExit(78)
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        identity = await bot.get_me()
        if (identity.username or "").lower() != EXPECTED_USERNAME:
            logging.error("Telegram getMe identity mismatch; refusing to poll another bot")
            raise SystemExit(78)  # permanent configuration error: no restart loop

        dp = Dispatcher()

        @dp.message(CommandStart())
        async def start(message: Message) -> None:
            if message.chat.type != "private" or not message.from_user:
                return
            locale = await observe_start(message, BOT_ID)
            caption, buttons = welcome_copy(locale), welcome_keyboard(locale)
            if WELCOME_IMAGE.is_file():
                try:
                    await message.answer_photo(
                        FSInputFile(WELCOME_IMAGE), caption=caption, reply_markup=buttons,
                    )
                    return
                except Exception:
                    logging.warning("%s welcome image unavailable; using text fallback", BOT_ID)
            await message.answer(caption, reply_markup=buttons)

        logging.info("%s online as @%s", BOT_ID, identity.username)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
