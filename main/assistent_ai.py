import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import BOT_TOKEN
from document_parser import extract_text_from_pdf, extract_text_from_docx
from llm import analyze_document

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "📄 Отправь PDF или DOCX документ — я сделаю отчет"
    )

print("🤖 Бот запущен и готов к работе.")

@dp.message(F.document)
async def handle_document(message: Message):
    doc = message.document
    file_path = f"temp_{doc.file_name}"

    await bot.download(doc, destination=file_path)

    if doc.file_name.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif doc.file_name.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        await message.answer("❌ Поддерживаются только PDF и DOCX")
        return
    print("🔍 Анализирую документ...")
    await message.answer("🔍 Анализирую документ...")

    result = await analyze_document(text)

    if result is None or result.strip() == "":
        print("⚠️ Не удалось получить ответ от модели.")
        await message.answer("⚠️ Не удалось получить ответ от модели.")
    else:
        print("✅ Анализ завершен.")
        await message.answer(result)

    os.remove(file_path)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
