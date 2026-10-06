from processing.cleaning import clean_price, clean_rating, clean_text, clean_url


def test_clean_text():
    assert clean_text("  Hello   world ") == "Hello world"


def test_clean_price():
    assert clean_price("£12.50") == 12.50


def test_clean_rating():
    assert clean_rating("Five") == 5
    assert clean_rating("7") is None


def test_clean_url():
    assert clean_url("https://example.com/test") == "https://example.com/test"
    assert clean_url("not-a-url") is None
