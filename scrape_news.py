import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from urllib.parse import urljoin
import time
import re

# Configuration
BASE_URL = "https://cub.edu.bd/"
NEWS_PAGE = "https://cub.edu.bd/index_all_news.php"
DOWNLOAD_FOLDER = "news"

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': '',  # Change this to your MySQL password
    'database': 'canadian_university'
}

def create_download_folder():
    """Create the news download folder if it doesn't exist"""
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
        CREATE TABLE IF NOT EXISTS news (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            title VARCHAR(500),
            description TEXT,
            url VARCHAR(500),
            image_url VARCHAR(500),
            UNIQUE KEY unique_news (title, date)
        )
        """
        cursor.execute(create_table_query)
        print("Table 'news' is ready")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    
    return True

def download_image(url, filename):
    """Download an image from URL and save it to the news folder"""
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

def scrape_news():
    """Scrape all news from the news page"""
    try:
        print("Fetching news page...")
        response = requests.get(NEWS_PAGE, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all news cards
        news_cards = soup.find_all('div', class_='card')
        print(f"Found {len(news_cards)} news items")
        
        news_list = []
        
        for card in news_cards:
            try:
                # Extract title
                title_tag = card.find('h5', class_='card-title')
                title = title_tag.text.strip() if title_tag else "No title"
                
                # Extract description
                desc_tag = card.find('p', class_='card-text')
                description = desc_tag.text.strip() if desc_tag else ""
                
                # Extract date (format: YYYY-MM-DD)
                date_text = None
                text_content = card.get_text()
                date_match = re.search(r'\d{4}-\d{2}-\d{2}', text_content)
                if date_match:
                    date_text = date_match.group(0)
                
                # Extract URL
                link_tag = card.find('a', href=True)
                url = None
                if link_tag:
                    url = urljoin(BASE_URL, link_tag['href'])
                
                # Extract image URL
                img_tag = card.find('img', class_='card-img-top')
                image_url = None
                if img_tag:
                    # Try 'src' first, then 'data-src' for lazy loading
                    image_url = img_tag.get('src') or img_tag.get('data-src')
                    if image_url:
                        image_url = urljoin(BASE_URL, image_url)
                
                if title and date_text:
                    news_list.append({
                        'title': title,
                        'date': date_text,
                        'description': description,
                        'url': url or '',
                        'image_url': image_url or ''
                    })
                    print(f"Extracted: {title[:50]}... | {date_text}")
                else:
                    print(f"Skipping incomplete news: {title}")
            
            except Exception as e:
                print(f"Error processing card: {e}")
                continue
        
        return news_list
    
    except Exception as e:
        print(f"Error scraping news: {e}")
        return []

def save_to_database(news_data):
    """Save scraped news to MySQL database"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO news (date, title, description, url, image_url)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            description = VALUES(description),
            url = VALUES(url),
            image_url = VALUES(image_url)
        """
        
        for news_item in news_data:
            cursor.execute(insert_query, (
                news_item['date'],
                news_item['title'],
                news_item['description'],
                news_item['url'],
                news_item['image_url']
            ))
        
        conn.commit()
        print(f"Saved {len(news_data)} news items to database")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

def main():
    """Main function to orchestrate the scraping process"""
    print("=" * 60)
    print("CUB News Scraper")
    print("=" * 60)
    
    # Step 1: Create download folder
    create_download_folder()
    
    # Step 2: Setup database
    if not setup_database():
        print("Failed to setup database. Exiting...")
        return
    
    # Step 3: Scrape news
    news_list = scrape_news()
    
    if not news_list:
        print("No news found. Exiting...")
        return
    
    # Step 4: Download images and update image paths
    news_with_images = []
    
    for i, news_item in enumerate(news_list, 1):
        print(f"\nProcessing news {i}/{len(news_list)}: {news_item['title'][:50]}...")
        
        local_image_path = ''
        
        if news_item['image_url']:
            # Create a safe filename based on the title and date
            base_filename = f"{news_item['date']}_{sanitize_filename(news_item['title'][:50])}"
            
            # Get file extension from URL
            ext = '.jpg'  # default
            if news_item['image_url']:
                url_parts = news_item['image_url'].split('.')
                if len(url_parts) > 1:
                    ext = '.' + url_parts[-1].split('?')[0]  # Remove query params
            
            filename = base_filename + ext
            
            # Download the image
            local_path = download_image(news_item['image_url'], filename)
            
            if local_path:
                local_image_path = local_path
        
        news_with_images.append({
            'title': news_item['title'],
            'date': news_item['date'],
            'description': news_item['description'],
            'url': news_item['url'],
            'image_url': local_image_path  # Store local path instead of URL
        })
        
        # Be nice to the server
        time.sleep(0.5)
    
    # Step 5: Save to database
    save_to_database(news_with_images)
    
    print("\n" + "=" * 60)
    print("Scraping completed!")
    print(f"Total news processed: {len(news_with_images)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
