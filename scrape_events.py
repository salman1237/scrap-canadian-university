import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from urllib.parse import urljoin
import time
import re

# Configuration
BASE_URL = "https://cub.edu.bd/"
EVENTS_PAGE = "https://cub.edu.bd/index_all_events.php"
DOWNLOAD_FOLDER = "events"

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': '',  # Change this to your MySQL password
    'database': 'canadian_university'
}

def create_download_folder():
    """Create the events download folder if it doesn't exist"""
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
        CREATE TABLE IF NOT EXISTS events (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500),
            description TEXT,
            url VARCHAR(500),
            image_url VARCHAR(500),
            date DATE,
            time VARCHAR(100),
            UNIQUE KEY unique_event (title, date)
        )
        """
        cursor.execute(create_table_query)
        print("Table 'events' is ready")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    
    return True

def download_image(url, filename):
    """Download an image from URL and save it to the events folder"""
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

def scrape_events():
    """Scrape all events from the events page"""
    try:
        print("Fetching events page...")
        response = requests.get(EVENTS_PAGE, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all event cards
        event_cards = soup.find_all('div', class_='card')
        print(f"Found {len(event_cards)} events")
        
        events_list = []
        
        for card in event_cards:
            try:
                # Extract title
                title_tag = card.find('h6')
                title = title_tag.text.strip() if title_tag else "No title"
                
                # Extract description (from small.card-text, excluding the anchor tag)
                desc_tag = card.find('small', class_='card-text')
                description = ""
                if desc_tag:
                    # Get text but exclude the "View more" link
                    for element in desc_tag.find_all('a'):
                        element.decompose()  # Remove anchor tags
                    description = desc_tag.text.strip()
                
                # Extract URL
                link_tag = card.find('a', class_='btn-danger')
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
                
                # Extract date and time from the paragraph
                p_tag = card.find('p')
                date_text = None
                time_text = None
                
                if p_tag:
                    # Get all text content
                    text_content = p_tag.get_text()
                    
                    # Extract date (format: YYYY-MM-DD)
                    date_match = re.search(r'\d{4}-\d{2}-\d{2}', text_content)
                    if date_match:
                        date_text = date_match.group(0)
                    
                    # Extract time (look for time patterns like "10:00 AM" or "02:30 PM")
                    # The time is in a span tag after the clock icon
                    span_tag = p_tag.find('span')
                    if span_tag:
                        time_text = span_tag.text.strip()
                    else:
                        # Fallback: try to find time pattern in text
                        time_match = re.search(r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?', text_content)
                        if time_match:
                            time_text = time_match.group(0)
                
                if title and date_text:
                    events_list.append({
                        'title': title,
                        'description': description,
                        'url': url or '',
                        'image_url': image_url or '',
                        'date': date_text,
                        'time': time_text or ''
                    })
                    print(f"Extracted: {title[:50]}... | {date_text} | {time_text}")
                else:
                    print(f"Skipping incomplete event: {title} (missing date)")
            
            except Exception as e:
                print(f"Error processing card: {e}")
                continue
        
        return events_list
    
    except Exception as e:
        print(f"Error scraping events: {e}")
        return []

def save_to_database(events_data):
    """Save scraped events to MySQL database"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO events (title, description, url, image_url, date, time)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            description = VALUES(description),
            url = VALUES(url),
            image_url = VALUES(image_url),
            time = VALUES(time)
        """
        
        for event in events_data:
            cursor.execute(insert_query, (
                event['title'],
                event['description'],
                event['url'],
                event['image_url'],
                event['date'],
                event['time']
            ))
        
        conn.commit()
        print(f"Saved {len(events_data)} events to database")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

def main():
    """Main function to orchestrate the scraping process"""
    print("=" * 60)
    print("CUB Events Scraper")
    print("=" * 60)
    
    # Step 1: Create download folder
    create_download_folder()
    
    # Step 2: Setup database
    if not setup_database():
        print("Failed to setup database. Exiting...")
        return
    
    # Step 3: Scrape events
    events_list = scrape_events()
    
    if not events_list:
        print("No events found. Exiting...")
        return
    
    # Step 4: Download images and update image paths
    events_with_images = []
    
    for i, event in enumerate(events_list, 1):
        print(f"\nProcessing event {i}/{len(events_list)}: {event['title'][:50]}...")
        
        local_image_path = ''
        
        if event['image_url']:
            # Create a safe filename based on the title and date
            base_filename = f"{event['date']}_{sanitize_filename(event['title'][:50])}"
            
            # Get file extension from URL
            ext = '.jpg'  # default
            if event['image_url']:
                url_parts = event['image_url'].split('.')
                if len(url_parts) > 1:
                    ext = '.' + url_parts[-1].split('?')[0]  # Remove query params
            
            filename = base_filename + ext
            
            # Download the image
            local_path = download_image(event['image_url'], filename)
            
            if local_path:
                local_image_path = local_path
        
        events_with_images.append({
            'title': event['title'],
            'description': event['description'],
            'url': event['url'],
            'image_url': local_image_path,  # Store local path instead of URL
            'date': event['date'],
            'time': event['time']
        })
        
        # Be nice to the server
        time.sleep(0.5)
    
    # Step 5: Save to database
    save_to_database(events_with_images)
    
    print("\n" + "=" * 60)
    print("Scraping completed!")
    print(f"Total events processed: {len(events_with_images)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
