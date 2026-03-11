from bs4 import BeautifulSoup
from fetcher import create_session, fetch_page
from futbol24.checkpoint import load_checkpoint, save_checkpoint
from parser import parse_listings
from urllib.parse import urljoin
import time
import random
import os
import logging
from log_config import setup_logging
from database import create_connection, create_table, insert_listing
from clean import clean_price, clean_bedrooms, clean_bathrooms, clean_parking_spaces, clean_size
 
base_url="https://www.property24.co.ke/property-to-rent-in-nairobi-c1890?Page={}"
failed_pages=[]
empty_pages=[]
consequtive_existing_records_threshold=50

setup_logging()
logger=logging.getLogger(__name__)

folder_path = 'checkpoint'
os.makedirs(folder_path, exist_ok=True)
checkpoint_path= os.path.join(folder_path, 'checkpoint.txt')

conn = create_connection()
create_table(conn)

def main():
    #create session ,get the page and extract the  last page number
    session=create_session()
    response=session.get(base_url.format(1),timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination=soup.find('ul',class_='pagination').find_all('li')
    last_page=int(pagination[-1].text.strip())
    logger.info(f"last_page: {last_page}")
    #iterate through pages and extract listings
    last_page_scrapped=load_checkpoint(checkpoint_path)
    duplicate_count=0
    for page in range(last_page_scrapped, last_page+1):
        inserted_count=0
        rel_url=base_url.format(page)
        response=fetch_page(session, rel_url)
        #!!!!!!add function to validate page content for potential access issues or CAPTCHAs by checking for specific keywords in the text content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        attrs_list=parse_listings(soup)
        if not attrs_list:
            logger.info(f"No listings parsed on page {page} with URL: {rel_url}.")
            empty_pages.append(page)
            continue
        for attrs in attrs_list:
            attrs['page_number']=page
            attrs['listing_link']=urljoin(base_url.format(page), attrs['listing_link'])
            attrs['price']=clean_price(attrs['price'])
            attrs['bedrooms']=clean_bedrooms(attrs['bedrooms'])
            attrs['bathrooms']=clean_bathrooms(attrs['bathrooms'])
            attrs['parking_spaces']=clean_parking_spaces(attrs['parking_spaces'])
            attrs['size']=clean_size(attrs['size'])
        for listing in attrs_list:
            before_insertion_count=conn.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
            insert_listing(conn, listing)
            after_insertion_count=conn.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
            if after_insertion_count > before_insertion_count:
                inserted_count += 1
                duplicate_count=0
            else:
                duplicate_count += 1
        logger.info(f"Page {page}: Parsed {len(attrs_list)} listings, Inserted {inserted_count} new listings.")
        if duplicate_count >= consequtive_existing_records_threshold:
            logger.warning(f"Warning: Detected {duplicate_count} consecutive existing records. This may indicate that the scraper is encountering duplicate data or has reached the end of new listings.")
            break
        #save file checkpoint after each page
        save_checkpoint(page, checkpoint_path)
        delay=random.uniform(0, 2)
        time.sleep(delay)
        
    if os.path.exists(checkpoint_path):
        os.remove(checkpoint_path)
        logger.info('Clearing checkpoint file for next scheduled run.')
    
if __name__ == "__main__":
    main()
