# AI Usage

## Tool Used

ChatGPT

## Purpose

AI assistance was used as a development aid for:

- planning the project structure
- reviewing the standardized data model
- discussing pagination strategies
- identifying possible validation cases
- reviewing error-handling scenarios
- suggesting unit-test cases
- improving README organization

## Representative Prompts

1. "Suggest a clean Python project structure for a multi-source web scraping assessment."
2. "How can Requests and BeautifulSoup handle pagination without hard-coding page URLs?"
3. "What validation checks are useful for a standardized scraping dataset?"
4. "Suggest unit tests for text cleaning, validation and duplicate detection."

## AI-Assisted Areas

The following areas received AI assistance during development:

- initial project organization
- implementation ideas for reusable cleaning functions
- validation test cases
- documentation wording
- edge-case review

## Human Review

The implementation was reviewed after generation. Source-specific selectors, field mappings, validation rules, duplicate keys, file paths, and test cases were checked against the assignment requirements.

The final design deliberately uses Requests + BeautifulSoup rather than browser automation because the provided websites are static scraping-practice sites.

## Verification

The project should be verified from a clean virtual environment by running:

```bash
pip install -r requirements.txt
pytest -q
python main.py
```

The resulting CSV and JSON report should then be inspected for:

- records from both sources
- standardized columns
- valid URLs
- numeric prices
- ratings within the expected range
- duplicate count
- final record count

## Important Note

AI-generated suggestions were treated as development assistance rather than as authoritative output. Any generated implementation must be tested against the actual website structure before submission.
