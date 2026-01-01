# CUB News Scraper

This Python script scrapes news from the Canadian University of Bangladesh (CUB) website and stores them in a MySQL database.

## Features

- Scrapes all news from https://cub.edu.bd/index_all_news.php
- Extracts news title, date, description, URL, and image
- Downloads all news card images to a local `news` folder
- Stores all data in the existing MySQL database `canadian_university`
- Handles duplicate entries (updates existing records)
- Error handling for network issues and missing data

## Requirements

- Python 3.7 or higher
- MySQL Server (localhost) with `canadian_university` database
- Required Python packages (already installed from notices scraper)

## Database Schema

The script creates a `news` table with the following structure:

```sql
CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    title VARCHAR(500),
    description TEXT,
    url VARCHAR(500),
    image_url VARCHAR(500),
    UNIQUE KEY unique_news (title, date)
);
```

## Usage

1. **Configure MySQL credentials** (same as notices scraper):
   Update the credentials in `scrape_news.py`:
   ```python
   MYSQL_CONFIG = {
       'host': 'localhost',
       'user': 'root',  # Change this to your MySQL username
       'password': '',  # Change this to your MySQL password
       'database': 'canadian_university'
   }
   ```

2. **Run the script:**
   ```bash
   python scrape_news.py
   ```

## What It Does

1. Creates a `news` folder for downloading images
2. Creates the `news` table (if it doesn't exist)
3. Scrapes all news from the website (164 news items)
4. For each news item:
   - Extracts title, date, description, URL, and image URL
   - Downloads the news card image
   - Saves the local image path
5. Stores all data in the MySQL database

## Output

The script stores:
- **date**: Publication date in YYYY-MM-DD format
- **title**: News headline
- **description**: News summary/description
- **url**: Link to full news article (e.g., `news_post.php?title=...`)
- **image_url**: Local path to downloaded image (e.g., `news/2025-12-15_Holiday_Notice.jpg`)

## Error Handling

- Network timeouts and connection errors are handled gracefully
- Missing or incomplete data is skipped with warnings
- Failed downloads still save the news metadata
- Duplicate titles on the same date update existing records instead of causing errors

## Notes

- The script includes a 0.5-second delay between requests
- All images are saved with sanitized filenames based on date and title
- The `image_url` column stores the local file path, not the original URL
- The UNIQUE constraint on (title, date) prevents duplicate entries
