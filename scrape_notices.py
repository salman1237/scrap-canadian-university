import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from urllib.parse import urljoin
import time

# Configuration
BASE_URL = "https://cub.edu.bd/"
NOTICES_PAGE = "https://cub.edu.bd/index_all_notice.php"
DOWNLOAD_FOLDER = "notices"

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': '',  # Change this to your MySQL password
    'database': 'canadian_university'
}

def create_download_folder():
    """Create the notices download folder if it doesn't exist"""
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
        print(f"Created folder: {DOWNLOAD_FOLDER}")
    else:
        print(f"Folder already exists: {DOWNLOAD_FOLDER}")

def setup_database():
    """Create database and table if they don't exist"""
    try:
        # Connect without specifying database first
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        print(f"Database '{MYSQL_CONFIG['database']}' is ready")
        
        conn.close()
        
        # Now connect to the specific database
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS notices (
            id VARCHAR(255) PRIMARY KEY,
            title VARCHAR(500),
            date DATE,
            attachment VARCHAR(500)
        )
        """
        cursor.execute(create_table_query)
        print("Table 'notices' is ready")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    
    return True

def download_file(url, filename):
    """Download a file from URL and save it to the notices folder"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {filename}")
        return filepath
    
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def get_attachment_url(detail_page_url):
    """Visit the notice detail page and get the actual attachment URL"""
    try:
        response = requests.get(detail_page_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the download button with class 'btn-outline-primary'
        download_btn = soup.find('a', class_='btn-outline-primary')
        
        if download_btn and download_btn.get('href'):
            attachment_url = urljoin(BASE_URL, download_btn['href'])
            return attachment_url
        
        return None
    
    except Exception as e:
        print(f"Error fetching detail page {detail_page_url}: {e}")
        return None

def scrape_notices():
    """Scrape all notices from the main page"""
    try:
        print("Fetching notices page...")
        response = requests.get(NOTICES_PAGE, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all notice cards
        notice_cards = soup.find_all('div', class_='card')
        print(f"Found {len(notice_cards)} notices")
        
        notices = []
        
        for card in notice_cards:
            try:
                # Extract title
                title_tag = card.find('h6')
                title = title_tag.text.strip() if title_tag else "No title"
                
                # Extract date and ID from the paragraph
                p_tag = card.find('p')
                
                if p_tag:
                    # Extract date (format: YYYY-MM-DD)
                    date_text = None
                    text_content = p_tag.get_text()
                    
                    # Look for date pattern (YYYY-MM-DD)
                    import re
                    date_match = re.search(r'\d{4}-\d{2}-\d{2}', text_content)
                    if date_match:
                        date_text = date_match.group(0)
                    
                    # Extract ID
                    small_tag = p_tag.find('small')
                    notice_id = None
                    if small_tag:
                        id_text = small_tag.text.strip()
                        if 'ID' in id_text:
                            notice_id = id_text.replace('ID :', '').replace('ID:', '').strip()
                    
                    # Extract detail page link
                    detail_link = p_tag.find('a', href=True)
                    detail_page_url = None
                    if detail_link:
                        detail_page_url = urljoin(BASE_URL, detail_link['href'])
                    
                    if notice_id and date_text and detail_page_url:
                        notices.append({
                            'id': notice_id,
                            'title': title,
                            'date': date_text,
                            'detail_url': detail_page_url
                        })
                        print(f"Extracted: {title} | {date_text} | {notice_id}")
                    else:
                        print(f"Skipping incomplete notice: {title}")
            
            except Exception as e:
                print(f"Error processing card: {e}")
                continue
        
        return notices
    
    except Exception as e:
        print(f"Error scraping notices: {e}")
        return []

def save_to_database(notices_data):
    """Save scraped notices to MySQL database"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO notices (id, title, date, attachment)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            date = VALUES(date),
            attachment = VALUES(attachment)
        """
        
        for notice in notices_data:
            cursor.execute(insert_query, (
                notice['id'],
                notice['title'],
                notice['date'],
                notice['attachment']
            ))
        
        conn.commit()
        print(f"Saved {len(notices_data)} notices to database")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

def main():
    """Main function to orchestrate the scraping process"""
    print("=" * 60)
    print("CUB Notice Scraper")
    print("=" * 60)
    
    # Step 1: Create download folder
    create_download_folder()
    
    # Step 2: Setup database
    if not setup_database():
        print("Failed to setup database. Exiting...")
        return
    
    # Step 3: Scrape notices
    notices = scrape_notices()
    
    if not notices:
        print("No notices found. Exiting...")
        return
    
    # Step 4: Download attachments and prepare data
    notices_with_attachments = []
    
    for i, notice in enumerate(notices, 1):
        print(f"\nProcessing notice {i}/{len(notices)}: {notice['title']}")
        
        # Get the actual attachment URL from detail page
        attachment_url = get_attachment_url(notice['detail_url'])
        
        if attachment_url:
            # Create a safe filename
            filename = f"{notice['id'].replace('/', '_')}.pdf"
            
            # Download the attachment
            filepath = download_file(attachment_url, filename)
            
            if filepath:
                notices_with_attachments.append({
                    'id': notice['id'],
                    'title': notice['title'],
                    'date': notice['date'],
                    'attachment': filepath
                })
            else:
                # If download failed, still save the notice without attachment
                notices_with_attachments.append({
                    'id': notice['id'],
                    'title': notice['title'],
                    'date': notice['date'],
                    'attachment': ''
                })
        else:
            # No attachment found
            notices_with_attachments.append({
                'id': notice['id'],
                'title': notice['title'],
                'date': notice['date'],
                'attachment': ''
            })
        
        # Be nice to the server
        time.sleep(1)
    
    # Step 5: Save to database
    save_to_database(notices_with_attachments)
    
    print("\n" + "=" * 60)
    print("Scraping completed!")
    print(f"Total notices processed: {len(notices_with_attachments)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
