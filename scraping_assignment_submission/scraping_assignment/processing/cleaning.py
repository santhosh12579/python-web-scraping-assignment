from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List
from urllib.parse import urlparse

from datetime import datetime, timezone


def clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text or None


def clean_price(value: Any) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)

    cleaned = str(value).replace("£", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def clean_rating(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return value if 1 <= value <= 5 else None

    mapping = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }
    text = str(value).strip().lower()
    if text in mapping:
        return mapping[text]

    try:
        number = int(float(text))
        return number if 1 <= number <= 5 else None
    except ValueError:
        return None


def clean_url(value: Any) -> str | None:
    if value is None:
        return None

    url = str(value).strip()
    parsed = urlparse(url)

    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return url

    return None


def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = {
        "source": clean_text(record.get("source")),
        "source_url": clean_url(record.get("source_url")),
        "name_or_title": clean_text(record.get("name_or_title")),
        "category": clean_text(record.get("category")),
        "price": clean_price(record.get("price")),
        "rating": clean_rating(record.get("rating")),
        "author": clean_text(record.get("author")),
        "tags": clean_text(record.get("tags")),
        "description": clean_text(record.get("description")),
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }

    return cleaned


def clean_records(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_record(record) for record in records]
