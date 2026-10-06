from __future__ import annotations

import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com/"
TIMEOUT = 15


class BooksScraper:
    """Scraper for Books to Scrape."""

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
            LOGGER.error("Books request failed: %s | %s", url, exc)
            return None

    @staticmethod
    def _rating(value: str) -> Optional[int]:
        mapping = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
        }
        return mapping.get(value.strip().lower())

    def _parse_book(self, article, page_url: str) -> Optional[Dict]:
        title_link = article.select_one("h3 a")
        price_node = article.select_one(".price_color")
        availability_node = article.select_one(".availability")
        rating_node = article.select_one("p.star-rating")
        image_node = article.select_one("img")

        if not title_link:
            LOGGER.warning("Skipping book with missing title link on %s", page_url)
            return None

        title = title_link.get("title") or title_link.get_text(" ", strip=True)
        product_url = urljoin(page_url, title_link.get("href", ""))

        rating = None
        if rating_node:
            classes = rating_node.get("class", [])
            rating_words = [item for item in classes if item.lower() != "star-rating"]
            if rating_words:
                rating = self._rating(rating_words[0])

        price = None
        if price_node:
            raw_price = price_node.get_text(" ", strip=True).replace("£", "").strip()
            try:
                price = float(raw_price)
            except ValueError:
                LOGGER.warning("Invalid book price: %r | %s", raw_price, product_url)

        availability = (
            availability_node.get_text(" ", strip=True)
            if availability_node
            else None
        )

        return {
            "source": "Books to Scrape",
            "source_url": product_url,
            "name_or_title": title,
            "category": None,
            "price": price,
            "rating": rating,
            "author": None,
            "tags": None,
            "description": None,
            "availability": availability,
        }

    def _parse_category(self, soup: BeautifulSoup) -> Optional[str]:
        breadcrumb = soup.select("ul.breadcrumb li a")
        if len(breadcrumb) >= 3:
            return breadcrumb[-1].get_text(" ", strip=True)
        return None

    def _enrich_book(self, record: Dict) -> Dict:
        """Visit the product page to obtain category and description."""
        soup = self._get(record["source_url"])
        if soup is None:
            return record

        record["category"] = self._parse_category(soup)

        description = soup.select_one("#product_description + p")
        if description:
            record["description"] = description.get_text(" ", strip=True)

        return record

    def scrape(self) -> List[Dict]:
        records: List[Dict] = []
        next_url = BASE_URL
        page_number = 0

        while next_url:
            page_number += 1
            LOGGER.info("Scraping Books page %d: %s", page_number, next_url)
            soup = self._get(next_url)
            if soup is None:
                next_url = None
                continue

            for article in soup.select("article.product_pod"):
                try:
                    record = self._parse_book(article, next_url)
                    if record:
                        records.append(self._enrich_book(record))
                except Exception:
                    LOGGER.exception("Unexpected book parsing error on %s", next_url)

            next_link = soup.select_one("li.next a")
            next_url = urljoin(next_url, next_link["href"]) if next_link else None

        LOGGER.info("Books scraper collected %d records", len(records))
        return records
