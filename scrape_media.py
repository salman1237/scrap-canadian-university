import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from urllib.parse import urljoin
import time
import re

# Configuration
BASE_URL = "https://cub.edu.bd/"
MEDIA_PAGE = "https://cub.edu.bd/all_media.php"
DOWNLOAD_FOLDER = "media"

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': '',  # Change this to your MySQL password
    'database': 'canadian_university'
}

def create_download_folder():
    """Create the media download folder if it doesn't exist"""
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
        print(f"Created folder: {DOWNLOAD_FOLDER}")
    else:
        print(f"Folder already exists: {DOWNLOAD_FOLDER}")

def setup_database():
    """Create table if it doesn't exist"""
    try:
        # Connect to the database
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS media (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500),
            news_portal VARCHAR(255),
            url VARCHAR(500),
            image_url VARCHAR(500),
            date DATE,
            UNIQUE KEY unique_media (title, date)
        )
        """
        cursor.execute(create_table_query)
        print("Table 'media' is ready")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    
    return True

def download_image(url, filename):
    """Download an image from URL and save it to the media folder"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded image: {filename}")
        return filepath
    
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def sanitize_filename(filename):
    """Remove or replace invalid characters from filename"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def scrape_media():
    """Scrape all media from the media page"""
    try:
        print("Fetching media page...")
        response = requests.get(MEDIA_PAGE, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all media cards
        media_cards = soup.find_all('div', class_='card')
        print(f"Found {len(media_cards)} media items")
        
        media_list = []
        
        for card in media_cards:
            try:
                card_body = card.find('div', class_='card-body')
                if not card_body:
                    continue
                
                # Extract news portal (paragraph with style font-size: 12px)
                news_portal = ""
                portal_tag = card_body.find('p', style=re.compile('font-size.*12px'))
                if portal_tag:
                    news_portal = portal_tag.text.strip()
                
                # Extract title and URL (h6 inside an anchor tag)
                title_link = card_body.find('a', href=True)
                title = "No title"
                url = ""
                
                if title_link:
                    url = title_link['href']
                    # URL is external, so we don't need to join with BASE_URL
                    # unless it's a relative path
                    if not url.startswith('http'):
                        url = urljoin(BASE_URL, url)
                    
                    title_tag = title_link.find('h6', class_='card-title')
                    if title_tag:
                        title = title_tag.text.strip()
                
                # Extract image URL
                img_tag = card.find('img', class_='card-img-top')
                image_url = None
                if img_tag:
                    # Try 'src' first, then 'data-src' for lazy loading
                    image_url = img_tag.get('src') or img_tag.get('data-src')
                    if image_url:
                        image_url = urljoin(BASE_URL, image_url)
                
                # Extract date (inside a span tag)
                date_text = None
                span_tag = card_body.find('span')
                if span_tag:
                    date_str = span_tag.text.strip()
                    # Try to find date pattern YYYY-MM-DD
                    date_match = re.search(r'\d{4}-\d{2}-\d{2}', date_str)
                    if date_match:
                        date_text = date_match.group(0)
                
                # If date not found in span, search in all text content
                if not date_text:
                    text_content = card_body.get_text()
                    date_match = re.search(r'\d{4}-\d{2}-\d{2}', text_content)
                    if date_match:
                        date_text = date_match.group(0)
                
                if title and date_text:
                    media_list.append({
                        'title': title,
                        'news_portal': news_portal,
                        'url': url,
                        'image_url': image_url or '',
                        'date': date_text
                    })
                    print(f"Extracted: {title[:50]}... | {news_portal} | {date_text}")
                else:
                    print(f"Skipping incomplete media: {title} (missing date)")
            
            except Exception as e:
                print(f"Error processing card: {e}")
                continue
        
        return media_list
    
    except Exception as e:
        print(f"Error scraping media: {e}")
        return []

def save_to_database(media_data):
    """Save scraped media to MySQL database"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO media (title, news_portal, url, image_url, date)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            news_portal = VALUES(news_portal),
            url = VALUES(url),
            image_url = VALUES(image_url)
        """
        
        for media_item in media_data:
            cursor.execute(insert_query, (
                media_item['title'],
                media_item['news_portal'],
                media_item['url'],
                media_item['image_url'],
                media_item['date']
            ))
        
        conn.commit()
        print(f"Saved {len(media_data)} media items to database")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

def main():
    """Main function to orchestrate the scraping process"""
    print("=" * 60)
    print("CUB Media Scraper")
    print("=" * 60)
    
    # Step 1: Create download folder
    create_download_folder()
    
    # Step 2: Setup database
    if not setup_database():
        print("Failed to setup database. Exiting...")
        return
    
    # Step 3: Scrape media
    media_list = scrape_media()
    
    if not media_list:
        print("No media found. Exiting...")
        return
    
    # Step 4: Download images and update image paths
    media_with_images = []
    
    for i, media_item in enumerate(media_list, 1):
        print(f"\nProcessing media {i}/{len(media_list)}: {media_item['title'][:50]}...")
        
        local_image_path = ''
        
        if media_item['image_url']:
            # Create a safe filename based on the title and date
            base_filename = f"{media_item['date']}_{sanitize_filename(media_item['title'][:50])}"
            
            # Get file extension from URL
            ext = '.jpg'  # default
            if media_item['image_url']:
                url_parts = media_item['image_url'].split('.')
                if len(url_parts) > 1:
                    ext = '.' + url_parts[-1].split('?')[0]  # Remove query params
            
            filename = base_filename + ext
            
            # Download the image
            local_path = download_image(media_item['image_url'], filename)
            
            if local_path:
                local_image_path = local_path
        
        media_with_images.append({
            'title': media_item['title'],
            'news_portal': media_item['news_portal'],
            'url': media_item['url'],
            'image_url': local_image_path,  # Store local path instead of URL
            'date': media_item['date']
        })
        
        # Be nice to the server
        time.sleep(0.5)
    
    # Step 5: Save to database
    save_to_database(media_with_images)
    
    print("\n" + "=" * 60)
    print("Scraping completed!")
    print(f"Total media processed: {len(media_with_images)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
