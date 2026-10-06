from processing.deduplication import deduplicate_records


def test_duplicate_books_are_removed():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Example Book",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": " example   book ",
        },
    ]

    unique, duplicate_count = deduplicate_records(records)

    assert len(unique) == 1
    assert duplicate_count == 1
