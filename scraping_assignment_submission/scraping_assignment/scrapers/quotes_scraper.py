from __future__ import annotations

import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

BASE_URL = "https://quotes.toscrape.com/"
TIMEOUT = 15


class QuotesScraper:
    """Scraper for Quotes to Scrape."""

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (compatible; ScrapingAssignment/1.0)"}
        )

    def _get(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as exc:
            LOGGER.error("Quotes request failed: %s | %s", url, exc)
            return None

    def _parse_quote(self, quote, page_url: str) -> Optional[Dict]:
        text_node = quote.select_one("span.text")
        author_node = quote.select_one("small.author")

        if not text_node or not author_node:
            LOGGER.warning("Skipping incomplete quote on %s", page_url)
            return None

        author = author_node.get_text(" ", strip=True)
        quote_text = text_node.get_text(" ", strip=True)

        author_link = quote.select_one("a[href*='/author/']")
        author_url = (
            urljoin(page_url, author_link.get("href", ""))
            if author_link
            else None
        )

        tags = [
            tag.get_text(" ", strip=True)
            for tag in quote.select("div.tags a.tag")
        ]

        return {
            "source": "Quotes to Scrape",
            "source_url": page_url,
            "name_or_title": quote_text,
            "category": None,
            "price": None,
            "rating": None,
            "author": author,
            "tags": ", ".join(tags) if tags else None,
            "description": None,
            "availability": None,
            "author_url": author_url,
        }

    def scrape(self) -> List[Dict]:
        records: List[Dict] = []
        next_url = BASE_URL
        page_number = 0

        while next_url:
            page_number += 1
            LOGGER.info("Scraping Quotes page %d: %s", page_number, next_url)
            soup = self._get(next_url)
            if soup is None:
                next_url = None
                continue

            for quote in soup.select("div.quote"):
                try:
                    record = self._parse_quote(quote, next_url)
                    if record:
                        records.append(record)
                except Exception:
                    LOGGER.exception("Unexpected quote parsing error on %s", next_url)

            next_link = soup.select_one("li.next a")
            next_url = urljoin(next_url, next_link["href"]) if next_link else None

        LOGGER.info("Quotes scraper collected %d records", len(records))
        return records
