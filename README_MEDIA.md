# CUB Media Scraper

This Python script scrapes media coverage from the Canadian University of Bangladesh (CUB) website and stores them in a MySQL database.

## Features

- Scrapes all media coverage from https://cub.edu.bd/all_media.php
- Extracts media title, news portal, URL, image, and date
- Downloads all media card images to a local `media` folder
- Stores all data in the existing MySQL database `canadian_university`
- Handles duplicate entries (updates existing records)
- Error handling for network issues and missing data

## Requirements

- Python 3.7 or higher
- MySQL Server (localhost) with `canadian_university` database
- Required Python packages (already installed from previous scrapers)

## Database Schema

The script creates a `media` table with the following structure:

```sql
CREATE TABLE IF NOT EXISTS media (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500),
    news_portal VARCHAR(255),
    url VARCHAR(500),
    image_url VARCHAR(500),
    date DATE,
    UNIQUE KEY unique_media (title, date)
);
```

## Usage

1. **Configure MySQL credentials** (same as previous scrapers):
   Update the credentials in `scrape_media.py`:
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
   python scrape_media.py
   ```

## What It Does

1. Creates a `media` folder for downloading images
2. Creates the `media` table (if it doesn't exist)
3. Scrapes all media coverage from the website (62 media items)
4. For each media item:
   - Extracts title, news portal name, URL, image URL, and date
   - Downloads the media card image
   - Saves the local image path
5. Stores all data in the MySQL database

## Output

The script stores:
- **title**: Media headline/title
- **news_portal**: Name of the news portal (e.g., "The Daily Star", "Dhaka Tribune")
- **url**: Link to the full article on the external news portal
- **image_url**: Local path to downloaded image (e.g., `media/2025-12-15_Media_Title.jpg`)
- **date**: Publication date in YYYY-MM-DD format (DATE field)

## Error Handling

- Network timeouts and connection errors are handled gracefully
- Missing or incomplete data is skipped with warnings
- Failed downloads still save the media metadata
- Duplicate media (same title and date) update existing records instead of causing errors

## Notes

- The script includes a 0.5-second delay between requests
- All images are saved with sanitized filenames based on date and title
- The `image_url` column stores the local file path, not the original URL
- The UNIQUE constraint on (title, date) prevents duplicate entries
- News portal names are extracted from paragraph tags with specific styling
