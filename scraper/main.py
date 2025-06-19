# scraper/main.py

import os
import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_all_chapter_urls(start_url):
    urls = [start_url]
    while True:
        print(f"[INFO] Buscando próximo capítulo a partir de: {urls[-1]}")
        res = requests.get(urls[-1], headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        next_button = soup.select_one("a.next-part__button")
        if not next_button:
            print("[INFO] Nenhum próximo capítulo encontrado.")
            break

        next_url = "https://www.wattpad.com" + next_button.get("href")
        if next_url in urls:
            break
        urls.append(next_url)
        time.sleep(1)  # evita ser bloqueado
    return urls

def scrape_chapter(url):
    print(f"[INFO] Lendo capítulo: {url}")
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.select_one("h2").text.strip() if soup.select_one("h2") else "Sem título"
    content = "\n".join(p.text.strip() for p in soup.select("pre"))
    return {"url": url, "title": title, "text": content}

def main():
    start_url = os.environ.get("START_URL")
    if not start_url:
        raise Exception("Variável START_URL não definida")

    chapter_urls = get_all_chapter_urls(start_url)
    chapters = [scrape_chapter(url) for url in chapter_urls]

    with open("/app/shared/chapters.json", "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)

    print(f"[DONE] Total de capítulos salvos: {len(chapters)}")

if __name__ == "__main__":
    main()
