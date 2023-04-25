import os
import asyncio


import telegram
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)


async def send_notification(message_text: str) -> None:
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message_text)
