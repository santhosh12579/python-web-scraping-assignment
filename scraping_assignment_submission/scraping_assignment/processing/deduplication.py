from __future__ import annotations

import re
from typing import Dict, List, Tuple


def normalize_key_text(value) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip().lower())


def duplicate_key(record: Dict) -> Tuple:
    source = normalize_key_text(record.get("source"))

    if source == "books to scrape":
        return (
            source,
            normalize_key_text(record.get("name_or_title")),
        )

    if source == "quotes to scrape":
        return (
            source,
            normalize_key_text(record.get("name_or_title")),
            normalize_key_text(record.get("author")),
        )

    return (
        source,
        normalize_key_text(record.get("name_or_title")),
        normalize_key_text(record.get("author")),
    )


def deduplicate_records(records: List[Dict]) -> Tuple[List[Dict], int]:
    seen = set()
    unique: List[Dict] = []
    duplicates = 0

    for record in records:
        key = duplicate_key(record)
        if key in seen:
            duplicates += 1
            continue

        seen.add(key)
        unique.append(record)

    return unique, duplicates
