# Spoonacular API Documentation Scraper

This script scrapes the Spoonacular API documentation from https://spoonacular.com/food-api/docs and saves it in a structured JSON format.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the scraper:
```bash
python spoonacular_scraper.py
```

## Output

The scraper will create a `spoonacular_docs` directory containing JSON files for each documentation page. Each JSON file contains:
- Title of the page
- Description
- Endpoint details (parameters, responses, etc.)

## Features

- Automatically follows all documentation links
- Saves content in a structured JSON format
- Respects rate limiting (1 second delay between requests)
- Handles errors gracefully
- Avoids duplicate page scraping

## Note

Please be mindful of Spoonacular's terms of service and rate limits when using this scraper. 