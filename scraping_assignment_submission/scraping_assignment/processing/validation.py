from __future__ import annotations

from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse


def validate_record(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    if not record.get("source"):
        errors.append("missing_source")

    url = record.get("source_url")
    if not url:
        errors.append("missing_source_url")
    else:
        parsed = urlparse(str(url))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append("invalid_source_url")

    if not record.get("name_or_title"):
        errors.append("missing_name_or_title")

    price = record.get("price")
    if price is not None:
        if not isinstance(price, (int, float)) or price < 0:
            errors.append("invalid_price")

    rating = record.get("rating")
    if rating is not None:
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            errors.append("invalid_rating")

    return not errors, errors


def validate_records(records: List[Dict[str, Any]]) -> Tuple[List[Dict], List[Dict]]:
    valid: List[Dict] = []
    rejected: List[Dict] = []

    for record in records:
        is_valid, errors = validate_record(record)
        if is_valid:
            valid.append(record)
        else:
            rejected.append({"record": record, "errors": errors})

    return valid, rejected
