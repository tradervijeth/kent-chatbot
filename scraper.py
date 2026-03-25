"""
Scraper for University of Kent web pages.
Fetches and cleans HTML content from the configured URLs,
saving the extracted text to data/ for ingestion.

Usage:
    python scraper.py
"""

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from config import SCRAPE_URLS


def fetch_page(url):
    """Fetch a web page and return its HTML content."""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (compatible; UoKChatbot/1.0; "
                "student-project research)"
            )
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"  [ERROR] Failed to fetch {url}: {e}")
        return None


def extract_text(html, url):
    """
    Extract clean text content from HTML.
    Strips navigation, headers, footers, and scripts.
    Returns a dict with url, title, and content.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove non-content elements that would add noise
    for tag in soup(["nav", "header", "footer", "script", "style",
                     "noscript", "iframe", "form"]):
        tag.decompose()

    # Try to find the main content area
    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", {"role": "main"})
        or soup.find("div", class_="page-content")
    )

    content_source = main if main else soup.body if soup.body else soup

    # Extract title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else url

    # Get text, collapse whitespace
    text = content_source.get_text(separator="\n", strip=True)

    # Clean up: remove excessive blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned = "\n".join(lines)

    return {
        "url": url,
        "title": title,
        "content": cleaned,
    }


def scrape_all():
    """Scrape all configured URLs and return extracted content."""
    pages = []
    total = len(SCRAPE_URLS)

    for i, url in enumerate(SCRAPE_URLS, 1):
        print(f"[{i}/{total}] Scraping: {url}")
        html = fetch_page(url)

        if html:
            page_data = extract_text(html, url)
            word_count = len(page_data["content"].split())
            print(f"  -> {page_data['title']} ({word_count} words)")
            pages.append(page_data)
        else:
            print(f"  -> Skipped")

        # Be polite - don't hammer the server
        time.sleep(1)

    return pages


def main():
    """Run the scraper and save results to data/pages.json."""
    print("=" * 60)
    print("University of Kent Content Scraper")
    print("=" * 60)

    os.makedirs("data", exist_ok=True)
    pages = scrape_all()

    output_path = os.path.join("data", "pages.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2, ensure_ascii=False)

    total_words = sum(len(p["content"].split()) for p in pages)
    print(f"\nDone! Scraped {len(pages)} pages ({total_words} total words)")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
