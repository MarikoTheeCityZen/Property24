from bs4 import BeautifulSoup
from fetcher import create_session, fetch_page
from futbol24.checkpoint import load_checkpoint, save_checkpoint
from parser import parse_listings,expected_fields
import csv
from urllib.parse import urljoin
import time
import random
import os
base_url="https://www.property24.co.ke/property-to-rent-in-nairobi-c1890?Page={}"
failed_pages=[]
empty_pages=[]
folder_path = 'checkpoint'
os.makedirs(folder_path, exist_ok=True)
file_path= os.path.join(folder_path, 'checkpoint.txt')
def main():
    #create session ,get the page and extract the  last page number
    session=create_session()
    response=session.get(base_url.format(1),timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination=soup.find('ul',class_='pagination').find_all('li')
    last_page=int(pagination[-1].text.strip())
    print(f"last_page: {last_page}")
    #iterate through pages and extract listings
    last_page_scrapped=load_checkpoint(file_path)
    for page in range(last_page_scrapped, last_page+1):
        rel_url=base_url.format(page)
        response=fetch_page(session, rel_url)
        if not response:
            print(f"Failed to fetch page {page}")
            failed_pages.append(page)
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        attrs_list=parse_listings(soup)
        if not attrs_list:
            print(f"No listings parsed on page {page} with URL: {rel_url}.")
            empty_pages.append(page)
            #continue
        for attrs in attrs_list:
            attrs['page_number']=page
            attrs['listing_link']=urljoin(base_url.format(page), attrs['listing_link'])
        #append listings to CSV file
        with open('data/listings.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=expected_fields)
            if page == 1:
                writer.writeheader()
            writer.writerows(attrs_list)
        print(f"Page {page} processed with {len(attrs_list)} listings.")
        #save file checkpoint after each page
        save_checkpoint(page, file_path)
        delay=random.uniform(0, 2)
        time.sleep(delay)
if __name__ == "__main__":
    main()
