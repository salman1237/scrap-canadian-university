# CUB Web Scrapers

A comprehensive collection of Python web scrapers for the Canadian University of Bangladesh (CUB) website. This project extracts and stores data from five different sections of the CUB website into a MySQL database.

## Features

- **5 Complete Scrapers**: Notices, News, Events, Media, and Creatives
- **MySQL Integration**: All data stored in a single `canadian_university` database
- **File Downloads**: Automatically downloads PDF attachments and images
- **Duplicate Handling**: Smart updates for existing records
- **Error Resilient**: Comprehensive error handling for network issues and missing data
- **Idempotent**: Safe to run multiple times without creating duplicates

## Requirements

- Python 3.7 or higher
- MySQL Server running on localhost
- Internet connection

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure MySQL credentials:**
   
   Update the `MYSQL_CONFIG` dictionary in each scraper script:
   ```python
   MYSQL_CONFIG = {
       'host': 'localhost',
       'user': 'root',        # Your MySQL username
       'password': '',        # Your MySQL password
       'database': 'canadian_university'
   }
   ```

## Scrapers Overview

| # | Scraper | Script | URL | Table | Items | Downloads |
|---|---------|--------|-----|-------|-------|-----------|
| 1 | **Notices** | `scrape_notices.py` | [index_all_notice.php](https://cub.edu.bd/index_all_notice.php) | `notices` | Variable | PDF files → `notices/` |
| 2 | **News** | `scrape_news.py` | [index_all_news.php](https://cub.edu.bd/index_all_news.php) | `news` | 164 | Images → `news/` |
| 3 | **Events** | `scrape_events.py` | [index_all_events.php](https://cub.edu.bd/index_all_events.php) | `events` | 35 | Images → `events/` |
| 4 | **Media** | `scrape_media.py` | [all_media.php](https://cub.edu.bd/all_media.php) | `media` | 62 | Images → `media/` |
| 5 | **Creatives** | `scrape_creatives.py` | [creatives.php](https://cub.edu.bd/creatives.php) | `creatives` | 31 | Images → `creatives/` |

## Usage

### Running Individual Scrapers

Run any scraper by executing its Python script:

```bash
python scrape_notices.py
python scrape_news.py
python scrape_events.py
python scrape_media.py
python scrape_creatives.py
```

### Running All Scrapers

To scrape all content at once, run all scripts sequentially:

```bash
python scrape_notices.py && python scrape_news.py && python scrape_events.py && python scrape_media.py && python scrape_creatives.py
```

## Database Schema

All scrapers automatically create their respective tables in the `canadian_university` database.

### 1. Notices Table
```sql
CREATE TABLE notices (
    id VARCHAR(255) PRIMARY KEY,           -- Notice ID (e.g., "CUB/REG/Notice/...")
    title VARCHAR(500),
    date DATE,
    attachment VARCHAR(500)                -- Local path to PDF file
);
```

### 2. News Table
```sql
CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    title VARCHAR(500),
    description TEXT,
    url VARCHAR(500),
    image_url VARCHAR(500),                -- Local path to image
    UNIQUE KEY unique_news (title, date)
);
```

### 3. Events Table
```sql
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500),
    description TEXT,
    url VARCHAR(500),
    image_url VARCHAR(500),                -- Local path to image
    date DATE,
    time VARCHAR(100),
    UNIQUE KEY unique_event (title, date)
);
```

### 4. Media Table
```sql
CREATE TABLE media (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500),
    news_portal VARCHAR(255),              -- e.g., "The Daily Star"
    url VARCHAR(500),
    image_url VARCHAR(500),                -- Local path to image
    date DATE,
    UNIQUE KEY unique_media (title, date)
);
```

### 5. Creatives Table
```sql
CREATE TABLE creatives (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500),
    description TEXT,
    url VARCHAR(500),
    image_url VARCHAR(500),                -- Local path to image
    UNIQUE KEY unique_creative (title)
);
```

## How It Works

Each scraper follows the same workflow:

1. **Creates Download Folder**: Automatically creates a folder for downloaded files
2. **Sets Up Database**: Creates database and table if they don't exist
3. **Scrapes Data**: Fetches the webpage and extracts data using BeautifulSoup
4. **Downloads Files**: Downloads PDFs/images to local folders
5. **Stores in MySQL**: Saves all data to the database with duplicate handling

## Project Structure

```
ScrapCanadiaUniversity/
├── scrape_notices.py          # Scrapes notices (PDFs)
├── scrape_news.py             # Scrapes news articles
├── scrape_events.py           # Scrapes events
├── scrape_media.py            # Scrapes media coverage
├── scrape_creatives.py        # Scrapes creative works
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── notices/                   # Downloaded PDF attachments
├── news/                      # Downloaded news images
├── events/                    # Downloaded event images
├── media/                     # Downloaded media images
└── creatives/                 # Downloaded creative images
```

## Key Features

### Smart Duplicate Handling
All scrapers use `INSERT ... ON DUPLICATE KEY UPDATE` to:
- Insert new records
- Update existing records if already present
- Prevent database errors from duplicates

### Error Handling
- Network timeouts and connection errors are caught and logged
- Missing or incomplete data is skipped with warnings
- Failed downloads still save metadata without file paths
- Script continues even if individual items fail

### Rate Limiting
All scrapers include delays (0.5-1 second) between requests to:
- Be respectful to the server
- Avoid overwhelming the website
- Prevent potential IP blocking

### Local File Storage
- All downloaded files use sanitized filenames
- Filenames are based on date/title to be meaningful
- File paths stored in database are relative to project directory
- Supports re-running without re-downloading existing files

## Example Usage

### Query Notices
```sql
USE canadian_university;
SELECT title, date, attachment FROM notices ORDER BY date DESC LIMIT 10;
```

### Query Recent News
```sql
SELECT title, description, date FROM news 
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY date DESC;
```

### Query Upcoming Events
```sql
SELECT title, date, time FROM events 
WHERE date >= CURDATE()
ORDER BY date ASC;
```

### Query Media Coverage
```sql
SELECT title, news_portal, date FROM media 
ORDER BY date DESC;
```

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Verify username and password in `MYSQL_CONFIG`
- Check that the user has permissions to create databases and tables

### Download Errors
- Check internet connection
- Verify the CUB website is accessible
- Some files may be missing from the website (script will continue)

### Import Errors
- Run `pip install -r requirements.txt` to install all dependencies
- Ensure you're using Python 3.7 or higher

## Dependencies

- `requests==2.31.0` - HTTP library for web requests
- `beautifulsoup4==4.12.2` - HTML parsing library
- `mysql-connector-python==8.2.0` - MySQL database driver

## Notes

- The scrapers are designed to be run periodically to keep data up-to-date
- Each scraper can be run independently
- All scrapers use the same database but different tables
- Downloaded files are stored locally and paths are saved in the database
- The project covers all major public-facing content sections of the CUB website

## Statistics

- **Total Scrapers**: 5
- **Total Items**: 292+ entries
  - Notices: Variable
  - News: 164 items
  - Events: 35 items
  - Media: 62 items
  - Creatives: 31 items
- **Database Tables**: 5
- **Download Folders**: 5

## License

This project is for educational and archival purposes.
