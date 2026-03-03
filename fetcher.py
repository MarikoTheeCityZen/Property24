#import libraries
import time
import random
import requests
from requests.exceptions import HTTPError, ConnectionError,Timeout
#create session with headers
def create_session():
    session = requests.Session()
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'keep-alive': 'true',
    }
    session.headers.update(headers)
    return session
#fetch page with retry logic
def fetch_page(session, url,delay=2, retries=3):
    retryable_statuses = {500, 502, 503, 504,429}
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=15)
            if response.status_code == 200:
                return response
            if response.status_code in retryable_statuses:
                #check for Retry-After header for 429 Too Many Requests
                retry_after= response.headers.get('Retry-After')
                if retry_after and retry_after.isdigit():
                    delay = int(retry_after)+random.uniform(0, 1)
                    print(f"Received {response.status_code}. Retrying after {retry_after} seconds as per Retry-After header for URL: {url}")
                delay+=random.uniform(0, 1)
                print(f"Received {response.status_code}. Retrying after {delay} seconds for URL: {url}")
                time.sleep(delay)
                continue
            raise Exception(f"!retriable HTTP error: {response.status_code} for URL: {url}")
        except (HTTPError, ConnectionError, Timeout) as e:
            print(f"Attempt {attempt + 1}: Error fetching URL: {url} - {e}")
            time.sleep(delay+random.uniform(0, 1))
    raise Exception(f"Failed to fetch URL: {url} after {retries} attempts.")
