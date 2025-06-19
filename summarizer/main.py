import os
import json
import time
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise Exception("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)

chapters_path = "/app/shared/chapters.json"
print("[INIT] Waiting for chapters.json to appear...")
while not os.path.exists(chapters_path):
    print("[WAIT] chapters.json not found yet, waiting 2s...")
    time.sleep(2)

print("[LOAD] Reading chapters...")
with open(chapters_path, encoding="utf-8") as f:
    chapters = json.load(f)

print(f"[LOAD] {len(chapters)} chapters loaded.")

results = []

for i, chapter in enumerate(chapters):
    print(f"[PROCESS] Chapter {i + 1}/{len(chapters)}: {chapter['chapter']}")
    prompt = (
        f"Title: {chapter['chapter']}\n\n"
        f"Chapter text:\n{chapter['text']}\n\n"
        "Generate a summary in no more than 3 sentences, highlight the main events, "
        "and point out any possible issues or improvements in the text (spelling, cohesion, rhythm, etc)."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()
        results.append({
            "title": chapter["title"],
            "chapter": chapter["chapter"],
            "summary": result
        })
        print(f"[OK] Chapter {i + 1} summary generated.")
    except Exception as e:
        print(f"[ERROR] Failed to summarize chapter {i + 1}: {e}")
        results.append({
            "title": chapter["title"],
            "chapter": chapter["chapter"],
            "summary": "[ERROR generating summary]"
        })

output_path = "/app/shared/summaries.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"[DONE] {len(results)} summaries saved to {output_path}")
