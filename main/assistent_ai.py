import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from config import BOT_TOKEN
from document_parser import extract_text_from_pdf, extract_text_from_docx
from llm import analyze_document

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище текстов для каждого пользователя
user_data = {}

def get_analysis_kb():
    kb = [[KeyboardButton(text="📊 Сделать общий отчет")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(CommandStart())
async def start(message: Message):
    user_data[message.from_user.id] = [] # Очистка при старте
    await message.answer(
        "📄 Отправьте один или несколько документов.\n"
        "Затем нажмите кнопку для анализа.",
        reply_markup=get_analysis_kb()
    )

@dp.message(F.document)
async def handle_document(message: Message):
    uid = message.from_user.id
    if uid not in user_data:
        user_data[uid] = []

    doc = message.document
    file_path = f"temp_{uid}_{doc.file_name}"
    await bot.download(doc, destination=file_path)

    await message.answer(f"⏳ Читаю '{doc.file_name}'...")

    try:
        if doc.file_name.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif doc.file_name.endswith(".docx"):
            text = extract_text_from_docx(file_path)
        else:
            await message.answer("❌ Формат не поддерживается")
            return

        # Добавляем имя файла, чтобы ИИ мог сравнивать их между собой
        user_data[uid].append(f"FILENAME: {doc.file_name}\nCONTENT: {text}")
        # print(text)
        await message.answer(f"✅ Файл добавлен (Всего: {len(user_data[uid])})")
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@dp.message(F.text == "📊 Сделать общий отчет")
async def process_all(message: Message):
    uid = message.from_user.id
    docs = user_data.get(uid, [])

    if not docs:
        await message.answer("⚠️ Сначала отправьте хотя бы один документ.")
        return

    await message.answer("🔍 Анализирую связи между документами...")

    # Соединяем все документы в один большой текст
    full_text = "\n\n--- NEXT DOCUMENT ---\n\n".join(docs)
    
    # Отправляем в ИИ (он прочитает всё сразу)
    result = await analyze_document(full_text)

    if result:
        await message.answer(result)
        user_data[uid] = [] # Сброс после анализа
    else:
        await message.answer("⚠️ Ошибка анализа.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

