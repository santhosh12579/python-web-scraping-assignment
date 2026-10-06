from processing.validation import validate_record


def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Example",
        "price": 10.0,
        "rating": 4,
    }
    valid, errors = validate_record(record)
    assert valid is True
    assert errors == []


def test_invalid_rating():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Example",
        "price": 10.0,
        "rating": 6,
    }
    valid, errors = validate_record(record)
    assert valid is False
    assert "invalid_rating" in errors
