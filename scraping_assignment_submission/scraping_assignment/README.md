# Multi-Source Web Scraping & Data Consolidation

## 1. Overview

This project implements a reusable Python pipeline for collecting data from two public scraping-practice websites:

- Books to Scrape — https://books.toscrape.com/
- Quotes to Scrape — https://quotes.toscrape.com/

The pipeline performs:

1. Web scraping
2. Pagination
3. Data cleaning
4. Standardization
5. Validation
6. Duplicate detection
7. Consolidation
8. CSV generation
9. JSON summary generation
10. Logging

Only publicly accessible practice data is used. No authentication, CAPTCHA, access-control bypass, or restricted endpoint is used.

## 2. Python Version

Recommended: Python 3.11 or newer.

## 3. Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 4. Run

```bash
python main.py
```

The pipeline creates:

```text
output/final_dataset.csv
output/summary_report.json
logs/scraper.log
```

## 5. Scraping Approach

### Books

The scraper starts from the Books to Scrape home page and reads each page's `li.next a` link. It continues until no next-page link exists.

Each book listing is parsed for:

- title
- price
- availability
- rating
- product URL

The product page is then visited to obtain category and description.

### Quotes

The quote scraper starts from the Quotes to Scrape home page and follows the `li.next a` link until pagination ends.

Each quote contains:

- quote text
- author
- tags
- source page URL

## 6. Data Model

The consolidated CSV uses:

| Field | Description |
|---|---|
| source | Original website |
| source_url | Original record URL |
| name_or_title | Book title or quote text |
| category | Book category where available |
| price | Numeric price where available |
| rating | Rating from 1 to 5 where available |
| author | Quote author where available |
| tags | Quote tags where available |
| description | Book description where available |
| scraped_at | UTC timestamp |

Fields that do not apply to a source are stored as empty values.

## 7. Cleaning

Cleaning is kept separate from scraping.

The pipeline:

- removes leading/trailing whitespace
- collapses repeated whitespace
- converts prices to floats
- converts ratings to integers
- validates HTTP/HTTPS URLs
- converts empty text to null values
- adds a UTC scraping timestamp

## 8. Validation

Records are rejected when required information is missing or invalid.

Validation checks include:

- source exists
- source URL exists and has a valid HTTP/HTTPS structure
- name/title exists
- price is numeric and non-negative when present
- rating is an integer from 1 to 5 when present

Rejected records and reasons are counted in the summary.

## 9. Deduplication

Deduplication is source-aware.

Books use:

```text
source + normalized title
```

Quotes use:

```text
source + normalized quote text + normalized author
```

Text is normalized by trimming whitespace, collapsing repeated whitespace, and converting to lowercase.

This avoids treating values such as:

```text
Example Book
 example   book
EXAMPLE BOOK
```

as different records.

Duplicates are removed before the final CSV is written, and the count is recorded in `summary_report.json`.

## 10. Error Handling

The scrapers use:

- request timeouts
- HTTP status checking
- exception handling
- page-level error logging
- missing-element checks
- invalid-value handling

A failure on one page does not intentionally terminate the entire application. The affected page is logged and the scraper continues where pagination information remains available.

## 11. Logging

Logs are written to:

```text
logs/scraper.log
```

They include page progress, request failures, parsing issues, record counts, duplicate counts, and pipeline completion time.

## 12. Tests

Run:

```bash
pytest -q
```

The tests cover:

- text cleanup
- price conversion
- rating conversion
- URL validation
- record validation
- duplicate detection

## 13. Assumptions

- The websites retain their public practice-site structure.
- Missing source-specific fields are represented as empty values.
- A book title uniquely identifies a book within Books to Scrape for this assignment.
- A quote text + author identifies a quote within Quotes to Scrape.
- The assignment does not require bypassing any site restriction.

## 14. Known Limitations

This is an assessment-scale scraper rather than a production crawler.

For production, I would add configurable rate limiting, persistent retries, checkpointing, monitoring, schema versioning, structured metrics, and stronger integration tests.

## 15. AI Usage

AI assistance was used during development for brainstorming implementation structure, debugging ideas, and documentation review. The final implementation was reviewed, tested, and adjusted manually. See `AI_USAGE.md` for details.

## 16. Design Decisions

Requests + BeautifulSoup was selected because both target websites are server-rendered HTML pages and do not require browser automation. This keeps the implementation lightweight, easy to reproduce, and easy to explain during an interview.

The scraper, processing, and validation responsibilities are separated so that source-specific changes do not require rewriting the complete pipeline.
