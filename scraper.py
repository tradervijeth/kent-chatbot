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

def extract_links(soup, base_domain="kent.ac.uk"):
    """Extract internal Kent links from a page for crawling."""
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if base_domain in href and href.startswith("http"):
            if not any(href.endswith(ext) for ext in [".pdf", ".jpg", ".png", ".zip"]):
                links.add(href.split("#")[0].split("?")[0])
    return links


def scrape_all():
    """Scrape all configured URLs and discover new links."""
    pages = []
    seen_urls = set(SCRAPE_URLS)
    discovered = []
    total = len(SCRAPE_URLS)

    for i, url in enumerate(SCRAPE_URLS, 1):
        print(f"[{i}/{total}] Scraping: {url}")
        html = fetch_page(url)

        if html:
            soup = BeautifulSoup(html, "html.parser")
            page_data = extract_text(html, url)
            word_count = len(page_data["content"].split())
            print(f"  -> {page_data['title']} ({word_count} words)")
            pages.append(page_data)

            # Discover new internal links
            for link in extract_links(soup):
                if link not in seen_urls:
                    seen_urls.add(link)
                    discovered.append(link)
        else:
            print(f"  -> Skipped")

        time.sleep(1)

    # Scrape discovered pages (capped at 50 to stay within limits)
    cap = min(len(discovered), 50)
    print(f"\nDiscovered {len(discovered)} new links, scraping up to {cap}...")
    for i, url in enumerate(discovered[:cap], 1):
        print(f"[Extra {i}/{cap}] Scraping: {url}")
        html = fetch_page(url)
        if html:
            page_data = extract_text(html, url)
            word_count = len(page_data["content"].split())
            print(f"  -> {page_data['title']} ({word_count} words)")
            pages.append(page_data)
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
