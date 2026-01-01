# CUB Creatives Scraper

This Python script scrapes creative works from the Canadian University of Bangladesh (CUB) website and stores them in a MySQL database.

## Features

- Scrapes all creative works from https://cub.edu.bd/creatives.php
- Extracts creative title, description, URL, and image
- Downloads all creative card images to a local `creatives` folder
- Stores all data in the existing MySQL database `canadian_university`
- Handles duplicate entries (updates existing records)
- Error handling for network issues and missing data

## Requirements

- Python 3.7 or higher
- MySQL Server (localhost) with `canadian_university` database
- Required Python packages (already installed from previous scrapers)

## Database Schema

The script creates a `creatives` table with the following structure:

```sql
CREATE TABLE IF NOT EXISTS creatives (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500),
    description TEXT,
    url VARCHAR(500),
    image_url VARCHAR(500),
    UNIQUE KEY unique_creative (title)
);
```

## Usage

1. **Configure MySQL credentials** (same as previous scrapers):
   Update the credentials in `scrape_creatives.py`:
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
   python scrape_creatives.py
   ```

## What It Does

1. Creates a `creatives` folder for downloading images
2. Creates the `creatives` table (if it doesn't exist)
3. Scrapes all creative works from the website (31 creative items)
4. For each creative:
   - Extracts title, description, URL, and image URL
   - Downloads the creative card image
   - Saves the local image path
5. Stores all data in the MySQL database

## Output

The script stores:
- **title**: Creative work title/headline
- **description**: Brief description or excerpt of the creative work
- **url**: Link to the full creative post (e.g., `creatives_post.php?title=...`)
- **image_url**: Local path to downloaded image (e.g., `creatives/Creative_Title.jpg`)

## Error Handling

- Network timeouts and connection errors are handled gracefully
- Missing or incomplete data is skipped with warnings
- Failed downloads still save the creative metadata
- Duplicate creatives (same title) update existing records instead of causing errors

## Notes

- The script includes a 0.5-second delay between requests
- All images are saved with sanitized filenames based on the title
- The `image_url` column stores the local file path, not the original URL
- The UNIQUE constraint on title prevents duplicate entries
- Titles are extracted from `<h6><strong>` tags within the card body
