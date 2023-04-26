import os

from django_q.tasks import schedule
import telebot
from django.utils import timezone
from dotenv import load_dotenv

from borrowing_service.models import Borrowing

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)


def send_notification(message_text: str) -> None:
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message_text)


def get_overdue_info():
    overdue = timezone.now()
    return Borrowing.objects.filter(expected_return_date__lte=overdue)


def make_massage(instance):
    return (
        "Overdue!\n"
        f"email: {instance.customer.email}\n"
        f"book: {instance.book.title}\n"
        f"expected return date: {instance.expected_return_date.strftime('%Y-%m-%d %H:%M')}\n"
    )


def overdue_sender():
    if get_overdue_info():
        for instance in get_overdue_info():
            message = make_massage(instance)
            send_notification(message)
    else:
        send_notification("No overdue!")


schedule(
    "clocked",
    overdue_sender(),
    name="overdue_sender",
    every=10,
    minutes=1,
    repeat=None,
    timeout=None,
    verbose=1,
)
