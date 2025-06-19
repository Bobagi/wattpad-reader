# summarizer/main.py
import json
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY")

with open("/app/shared/chapters.json", encoding="utf-8") as f:
    chapters = json.load(f)

results = []

for chapter in chapters:
    prompt = (
        f"Resumo breve do capítulo: {chapter['title']}.\n\n"
        f"Texto:\n{chapter['text']}\n\n"
        "Gere um resumo com 3 frases, destaque os principais acontecimentos e indique erros ou melhorias possíveis no texto."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    results.append({
        "title": chapter["title"],
        "summary": response.choices[0].message.content.strip()
    })

with open("/app/shared/summaries.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
