import google.genai as genai
from google.genai import types # Важно для настроек Gemini
import cohere
from openai import OpenAI
from config import GEMINI_API_KEY, COHERE_API_KEY, CROQ_API_KEY
from prompts import SYSTEM_PROMPT as system_prompt

# 1. Настройка Gemini (Новый SDK)
client_gemini = genai.Client(api_key=GEMINI_API_KEY)

# 2. Настройка Cohere
co = cohere.ClientV2(COHERE_API_KEY)

# 3. Настройка Groq (OpenAI-совместимый)
groq_client = OpenAI(
    api_key=CROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

async def analyze_document(text: str) -> str:
    # --- ПОПЫТКА 1: GROQ (Очень быстрый) ---
    # try:
    #     print("🔄 Попытка через Groq...")
    #     response = groq_client.responses.create(
    #         model="openai/gpt-oss-20b",
    #         input=[
    #             {"role": "system", "content": system_prompt},
    #             {"role": "user", "content": text}
    #         ],
    #         temperature=0.2
    #     )
    #     return response.output_text
    # except Exception as e:
    #     print(f"❌ Ошибка в Groq: {e}")

    # --- ПОПЫТКА 2: GEMINI (Большое окно контекста) ---
    try:
        print("🔄 Попытка через Gemini...")
        # В новом SDK конфиг передается вот так:
        response = client_gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2
            )
        )
        if response.text:
            return response.text
    except Exception as e:
        print(f"❌ Ошибка в Gemini: {e}")

    # --- ПОПЫТКА 3: COHERE (Надежный запасной вариант) ---
    try:
        print("🔄 Попытка через Cohere...")
        response = co.chat(
            model="command-a-03-2025",
            messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text} 
          ],
            temperature=0.2
        )
        return response.message.content[0].text
    except Exception as e:
        print(f"❌ Ошибка в Cohere: {e}")

    return "⚠️ К сожалению, все системы анализа сейчас перегружены. Попробуйте позже."