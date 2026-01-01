import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from urllib.parse import urljoin
import time
import re

# Configuration
BASE_URL = "https://cub.edu.bd/"
CREATIVES_PAGE = "https://cub.edu.bd/creatives.php"
DOWNLOAD_FOLDER = "creatives"

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': '',  # Change this to your MySQL password
    'database': 'canadian_university'
}

def create_download_folder():
    """Create the creatives download folder if it doesn't exist"""
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
        CREATE TABLE IF NOT EXISTS creatives (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500),
            description TEXT,
            url VARCHAR(500),
            image_url VARCHAR(500),
            UNIQUE KEY unique_creative (title)
        )
        """
        cursor.execute(create_table_query)
        print("Table 'creatives' is ready")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    
    return True

def download_image(url, filename):
    """Download an image from URL and save it to the creatives folder"""
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

def scrape_creatives():
    """Scrape all creatives from the creatives page"""
    try:
        print("Fetching creatives page...")
        response = requests.get(CREATIVES_PAGE, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all creative cards
        creative_cards = soup.find_all('div', class_='card')
        print(f"Found {len(creative_cards)} creative items")
        
        creatives_list = []
        
        for card in creative_cards:
            try:
                card_body = card.find('div', class_='card-body')
                if not card_body:
                    continue
                
                # Extract title (inside h6 > strong)
                title = "No title"
                title_tag = card_body.find('h6')
                if title_tag:
                    strong_tag = title_tag.find('strong')
                    if strong_tag:
                        title = strong_tag.text.strip()
                    else:
                        title = title_tag.text.strip()
                
                # Extract description (paragraph tag)
                description = ""
                desc_tag = card_body.find('p')
                if desc_tag:
                    description = desc_tag.text.strip()
                
                # Extract URL (anchor tag with "Click here")
                url = ""
                link_tag = card_body.find('a', href=True)
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
                
                if title and title != "No title":
                    creatives_list.append({
                        'title': title,
                        'description': description,
                        'url': url,
                        'image_url': image_url or ''
                    })
                    print(f"Extracted: {title[:50]}...")
                else:
                    print(f"Skipping incomplete creative (no title)")
            
            except Exception as e:
                print(f"Error processing card: {e}")
                continue
        
        return creatives_list
    
    except Exception as e:
        print(f"Error scraping creatives: {e}")
        return []

def save_to_database(creatives_data):
    """Save scraped creatives to MySQL database"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO creatives (title, description, url, image_url)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            description = VALUES(description),
            url = VALUES(url),
            image_url = VALUES(image_url)
        """
        
        for creative in creatives_data:
            cursor.execute(insert_query, (
                creative['title'],
                creative['description'],
                creative['url'],
                creative['image_url']
            ))
        
        conn.commit()
        print(f"Saved {len(creatives_data)} creative items to database")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

def main():
    """Main function to orchestrate the scraping process"""
    print("=" * 60)
    print("CUB Creatives Scraper")
    print("=" * 60)
    
    # Step 1: Create download folder
    create_download_folder()
    
    # Step 2: Setup database
    if not setup_database():
        print("Failed to setup database. Exiting...")
        return
    
    # Step 3: Scrape creatives
    creatives_list = scrape_creatives()
    
    if not creatives_list:
        print("No creatives found. Exiting...")
        return
    
    # Step 4: Download images and update image paths
    creatives_with_images = []
    
    for i, creative in enumerate(creatives_list, 1):
        print(f"\nProcessing creative {i}/{len(creatives_list)}: {creative['title'][:50]}...")
        
        local_image_path = ''
        
        if creative['image_url']:
            # Create a safe filename based on the title
            base_filename = sanitize_filename(creative['title'][:50])
            
            # Get file extension from URL
            ext = '.jpg'  # default
            if creative['image_url']:
                url_parts = creative['image_url'].split('.')
                if len(url_parts) > 1:
                    ext = '.' + url_parts[-1].split('?')[0]  # Remove query params
            
            filename = base_filename + ext
            
            # Download the image
            local_path = download_image(creative['image_url'], filename)
            
            if local_path:
                local_image_path = local_path
        
        creatives_with_images.append({
            'title': creative['title'],
            'description': creative['description'],
            'url': creative['url'],
            'image_url': local_image_path  # Store local path instead of URL
        })
        
        # Be nice to the server
        time.sleep(0.5)
    
    # Step 5: Save to database
    save_to_database(creatives_with_images)
    
    print("\n" + "=" * 60)
    print("Scraping completed!")
    print(f"Total creatives processed: {len(creatives_with_images)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
