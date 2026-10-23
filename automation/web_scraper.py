#!/usr/bin/env python3
import csv
import urllib.parse
import requests
from bs4 import BeautifulSoup

def fetch_and_parse(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"[X] Request error: {e}")
        return None

def scrape_links(soup, base_url, output_csv="scraped_data.csv"):
    if not soup: return
    data = []
    for idx, header in enumerate(soup.find_all(["h1", "h2", "h3"]), 1):
        text = header.get_text(strip=True)
        if not text: continue
        anchor = header.find("a") or header.find_parent("a")
        link = anchor["href"] if anchor and "href" in anchor.attrs else ""
        if link and not link.startswith(("http://", "https://")):
            link = urllib.parse.urljoin(base_url, link)
        data.append({"id": idx, "tag": header.name, "title": text, "url": link})
    if data:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"[✓] Scraped {len(data)} items to '{output_csv}'")

if __name__ == "__main__":
    target = "https://news.ycombinator.com/"
    scrape_links(fetch_and_parse(target), target)
