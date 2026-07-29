import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import CHECK_INTERVAL_MINUTES
from database import (
    init_db, is_news_sent, mark_news_sent,
    add_subscriber, remove_subscriber, get_all_subscribers
)
from news_parser import fetch_news
from ai_analyzer import analyze_news

logging.basicConfig(level=logging.INFO)

# Токен берём из "секретов"
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    add_subscriber(message.chat.id)
    await message.answer(
        "👋 Привет! Я бот-помощник для турагентства.\n\n"
        "Я слежу за новостями туризма и присылаю тебе важное "
        "с кратким нейро-анализом.\n\n"
        "✅ Ты подписан на рассылку!\n"
        "Команды:\n"
        "/stop — отписаться\n"
        "/check — проверить новости прямо сейчас"
    )


@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    remove_subscriber(message.chat.id)
    await message.answer("🔕 Ты отписался от рассылки. Напиши /start, чтобы вернуться.")


@dp.message(Command("check"))
async def cmd_check(message: Message):
    await message.answer("🔍 Проверяю свежие новости...")
    await check_and_send(target_chat=message.chat.id)


async def check_and_send(target_chat=None):
    """Проверяем новости и рассылаем подписчикам."""
    news_items = fetch_news()

    if target_chat:
        subscribers = [target_chat]
    else:
        subscribers = get_all_subscribers()

    if not subscribers:
        return

    found_new = False
    for news in news_items:
        # Для команды /check показываем даже старые, для авто — только новые
        if not target_chat and is_news_sent(news["link"]):
            continue

        found_new = True
        analysis = analyze_news(news["title"], news["summary"])

        text = (
            f"📰 <b>{news['title']}</b>\n\n"
            f"{analysis}\n\n"
            f"🔗 <a href='{news['link']}'>Читать источник</a>"
        )

        for chat_id in subscribers:
            try:
                await bot.send_message(chat_id, text, parse_mode="HTML")
            except Exception as e:
                logging.error(f"Не смог отправить {chat_id}: {e}")

        if not target_chat:
            mark_news_sent(news["link"])

        await asyncio.sleep(1)

    if target_chat and not found_new:
        await bot.send_message(target_chat, "😴 Свежих туристических новостей пока нет.")


async def scheduler():
    """Фоновая проверка новостей каждые N минут."""
    while True:
        try:
            await check_and_send()
        except Exception as e:
            logging.error(f"Ошибка в планировщике: {e}")
        await asyncio.sleep(CHECK_INTERVAL_MINUTES * 60)


async def main():
    init_db()
    asyncio.create_task(scheduler())
    logging.info("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
