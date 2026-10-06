from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import pandas as pd

from processing.cleaning import clean_records
from processing.deduplication import deduplicate_records
from processing.validation import validate_records
from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
LOG_DIR = ROOT / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

LOGGER = logging.getLogger("scraping_pipeline")


def run_pipeline() -> None:
    started = time.perf_counter()

    LOGGER.info("Starting multi-source scraping pipeline")

    books = BooksScraper().scrape()
    quotes = QuotesScraper().scrape()

    collected = {
        "Books to Scrape": len(books),
        "Quotes to Scrape": len(quotes),
    }

    raw_records = books + quotes
    LOGGER.info("Total records collected: %d", len(raw_records))

    cleaned_records = clean_records(raw_records)

    valid_records, rejected_records = validate_records(cleaned_records)
    LOGGER.info("Valid records: %d", len(valid_records))
    LOGGER.info("Rejected records: %d", len(rejected_records))

    unique_records, duplicate_count = deduplicate_records(valid_records)
    LOGGER.info("Duplicates detected: %d", duplicate_count)

    columns = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "scraped_at",
    ]

    dataframe = pd.DataFrame(unique_records, columns=columns)
    dataframe.to_csv(OUTPUT_DIR / "final_dataset.csv", index=False)

    after_cleaning = {
        "Books to Scrape": sum(
            1 for r in valid_records if r["source"] == "Books to Scrape"
        ),
        "Quotes to Scrape": sum(
            1 for r in valid_records if r["source"] == "Quotes to Scrape"
        ),
    }

    rejected_by_source = {
        "Books to Scrape": sum(
            1
            for item in rejected_records
            if item["record"].get("source") == "Books to Scrape"
        ),
        "Quotes to Scrape": sum(
            1
            for item in rejected_records
            if item["record"].get("source") == "Quotes to Scrape"
        ),
    }

    elapsed = round(time.perf_counter() - started, 2)

    summary = {
        "execution_time_seconds": elapsed,
        "records_collected": collected,
        "records_after_cleaning_and_validation": after_cleaning,
        "records_rejected": rejected_by_source,
        "duplicate_records_detected": duplicate_count,
        "final_record_count": len(unique_records),
        "output_file": "output/final_dataset.csv",
    }

    with open(OUTPUT_DIR / "summary_report.json", "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    LOGGER.info("Final dataset written to output/final_dataset.csv")
    LOGGER.info("Summary written to output/summary_report.json")
    LOGGER.info("Pipeline completed in %.2f seconds", elapsed)


if __name__ == "__main__":
    run_pipeline()
