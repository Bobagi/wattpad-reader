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
        print(f"[INFO] Fetching next chapter from: {urls[-1]}")
        res = requests.get(urls[-1], headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        nav_div = soup.find("div", id="story-part-navigation")
        if not nav_div:
            print("[INFO] Navigation div not found.")
            break

        next_link = nav_div.find("a")
        if not next_link or not next_link.get("href"):
            print("[INFO] No next chapter link found.")
            break

        next_url = next_link["href"]
        if not next_url.startswith("http"):
            next_url = "https://www.wattpad.com" + next_url

        if next_url in urls:
            break

        urls.append(next_url)
        time.sleep(1)

    return urls

def scrape_chapter(url):
    print(f"[INFO] Reading chapter: {url}")
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.select_one("h2").text.strip() if soup.select_one("h2") else "Untitled Book"
    
    h2_tags = soup.find_all(class_="h2")

    # for i, tag in enumerate(h2_tags):
    #     print(f"[DEBUG] h2[{i}]: {tag.text.strip()}")

    if len(h2_tags) >= 2:
        chapter = h2_tags[1].text.strip()
    elif h2_tags:
        chapter = h2_tags[0].text.strip()
    else:
        chapter = "Untitled Chapter"

    content = "\n".join(p.text.strip() for p in soup.select("pre"))
    return {"url": url, "title": title, "chapter": chapter, "text": content}

def main():
    start_url = os.environ.get("START_URL")
    if not start_url:
        raise Exception("START_URL environment variable not set")

    chapter_urls = get_all_chapter_urls(start_url)
    chapters = [scrape_chapter(url) for url in chapter_urls]

    with open("/app/shared/chapters.json", "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)

    print(f"[DONE] Total chapters saved: {len(chapters)}")

if __name__ == "__main__":
    main()
