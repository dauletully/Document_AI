import cohere
from config import AI_API_KEY
from prompts import SYSTEM_PROMPT as system_prompt

co = cohere.ClientV2(AI_API_KEY)

async def analyze_document(text: str) -> str:
    response = co.chat(
        model="command-a-03-2025",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text} 
        ],
        temperature=0.2
    ) 
    return response.message.content[0].text

    
