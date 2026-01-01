# CUB Events Scraper

This Python script scrapes events from the Canadian University of Bangladesh (CUB) website and stores them in a MySQL database.

## Features

- Scrapes all events from https://cub.edu.bd/index_all_events.php
- Extracts event title, description, URL, image, date, and time
- Downloads all event card images to a local `events` folder
- Stores all data in the existing MySQL database `canadian_university`
- Handles duplicate entries (updates existing records)
- Error handling for network issues and missing data

## Requirements

- Python 3.7 or higher
- MySQL Server (localhost) with `canadian_university` database
- Required Python packages (already installed from previous scrapers)

## Database Schema

The script creates an `events` table with the following structure:

```sql
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500),
    description TEXT,
    url VARCHAR(500),
    image_url VARCHAR(500),
    date DATE,
    time VARCHAR(100),
    UNIQUE KEY unique_event (title, date)
);
```

## Usage

1. **Configure MySQL credentials** (same as previous scrapers):
   Update the credentials in `scrape_events.py`:
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
   python scrape_events.py
   ```

## What It Does

1. Creates an `events` folder for downloading images
2. Creates the `events` table (if it doesn't exist)
3. Scrapes all events from the website (35 events)
4. For each event:
   - Extracts title, description, URL, image URL, date, and time
   - Downloads the event card image
   - Saves the local image path
5. Stores all data in the MySQL database

## Output

The script stores:
- **title**: Event headline
- **description**: Event summary/description
- **url**: Link to full event details (e.g., `event_details.php?...`)
- **image_url**: Local path to downloaded image (e.g., `events/2025-12-15_Event_Title.jpg`)
- **date**: Event date in YYYY-MM-DD format (DATE field)
- **time**: Event time (e.g., "10:00 AM", "02:30 PM")

## Error Handling

- Network timeouts and connection errors are handled gracefully
- Missing or incomplete data is skipped with warnings
- Failed downloads still save the event metadata
- Duplicate events (same title and date) update existing records instead of causing errors

## Notes

- The script includes a 0.5-second delay between requests
- All images are saved with sanitized filenames based on date and title
- The `image_url` column stores the local file path, not the original URL
- The UNIQUE constraint on (title, date) prevents duplicate entries
- Time is extracted from the span tag within the event card paragraph
