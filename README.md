# CUB Notice Scraper

This Python script scrapes notices from the Canadian University of Bangladesh (CUB) website and stores them in a MySQL database.

## Features

- Scrapes all notices from https://cub.edu.bd/index_all_notice.php
- Extracts notice title, date, and ID
- Downloads PDF attachments to a local `notices` folder
- Stores all data in a MySQL database
- Handles duplicate entries (updates existing records)
- Error handling for network issues and missing data

## Requirements

- Python 3.7 or higher
- MySQL Server (localhost)
- Required Python packages (see `requirements.txt`)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup MySQL:**
   - Make sure MySQL Server is running on localhost
   - Update the MySQL credentials in `scrape_notices.py`:
     ```python
     MYSQL_CONFIG = {
         'host': 'localhost',
         'user': 'root',  # Change this to your MySQL username
         'password': '',  # Change this to your MySQL password
         'database': 'canadian_university'
     }
     ```

## Usage

Run the script:
```bash
python scrape_notices.py
```

The script will:
1. Create a `notices` folder for downloading attachments
2. Create the `canadian_university` database (if it doesn't exist)
3. Create the `notices` table with the following structure:
   - `id` (VARCHAR 255) - PRIMARY KEY
   - `title` (VARCHAR 500)
   - `date` (DATE)
   - `attachment` (VARCHAR 500) - File path to downloaded PDF
4. Scrape all notices from the website
5. Download all attachments
6. Store everything in the database

## Database Schema

```sql
CREATE TABLE notices (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(500),
    date DATE,
    attachment VARCHAR(500)
);
```

## How It Works

1. The script fetches the main notices page
2. For each notice card, it extracts:
   - Title from the `<h6>` tag
   - Date (YYYY-MM-DD format)
   - Notice ID (e.g., CUB/REG/Notice/0025/20251215/01)
   - Link to the detail page
3. It visits each detail page to get the actual PDF download link
4. Downloads the PDF file and saves it to the `notices` folder
5. Stores all information in the MySQL database

## Error Handling

- Network timeouts and connection errors are handled gracefully
- Missing or incomplete data is skipped with warnings
- Failed downloads still save the notice metadata without attachment path
- Duplicate IDs update existing records instead of causing errors

## Notes

- The script includes a 1-second delay between requests to be respectful to the server
- All attachments are saved as PDFs in the `notices` folder with sanitized filenames
- The attachment path stored in the database is relative to the script location
