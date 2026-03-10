import re
#static fields to extract
expected_fields=['page_number', 'listing_number', 'title', 'location', 'address', 'description','bedrooms','bathrooms','parking spaces','size', 'price', 'listing_link', 'agency']
#error_fields=['access denied', 'captcha', 'not found', 'error','blocked','forbidden','unavailable','service unavailable']
#function to validate page content for potential access issues or CAPTCHAs by checking for specific keywords in the text content of the page

"""def validate_page(soup):
    text_content=soup.get_text(separator=' ', strip=True).lower()
    for error in error_fields:
        if re.search(r'\b'+re.escape(error)+r'\b', text_content):
            print(f"Warning: Detected '{error}' in page content. This may indicate a CAPTCHA or access issue.")
            return False
    if len(soup.text.strip()) < 10000:  # Arbitrary threshold for minimum content length
        print("Warning: Page content is unusually short. This may indicate a CAPTCHA or access issue.")
        return False
    if len(soup.find_all('div', class_='js_listingTile')) == 0:
        print("Warning: No listing tiles found on the page. This may indicate a CAPTCHA or access issue.")
        return False
    return True"""

#function to parse listings from a BeautifulSoup object
def parse_listings(soup):
    attrs_list=[]
    items=soup.find_all('div',class_='js_listingTile')
    #if the structure of the page has changed and no items are found, maybe a CAPTCHA or an empty page log a warning and return an empty list
    if not items:
        print("No listing items found on the page.")
        return attrs_list
    for item in items:
        attrs={col: None for col in expected_fields}
        listing_number=item.get('data-listing-number')
        attrs['listing_number']=listing_number
        content=item.find('span',class_="p24_content")
        title=content.find('span',class_='p24_propertyTitle')
        attrs['title']=title.get_text(strip=True) if title else None
        location=content.find('span',class_='p24_location')
        attrs['location']=location.get_text(strip=True) if location else None
        address=content.find('span',class_='p24_address')
        attrs['address']=address.get_text(strip=True) if address else None
        description=content.find('span',class_='p24_excerpt')
        attrs['description']=description.get_text(strip=True) if description else None
        features=content.find_all('span',class_='p24_featureDetails')
        if features:
            for feature in features:
                feature_name=feature.get('title').lower().strip()
                if feature_name in expected_fields:
                    feature_value=feature.get_text(strip=True)
                    attrs[feature_name]=feature_value
        size=content.find('span',class_='p24_size')
        attrs['size']=size.get_text(strip=True) if size else None
        price=content.find('span',class_='p24_price')
        attrs['price']=price.get_text(strip=True) if price else None
        listing_link=item.select_one('a').get('href')
        attrs['listing_link']=listing_link
        agency_container=content.find('span',class_='p24_branding')
        agency=agency_container.get('title') if agency_container else None
        attrs['agency']=agency
        attrs_list.append(attrs)
        #print(f"Parsed listing: {listing_number}")
    return attrs_list
