import pandas as pd
from main import failed_pages,empty_pages

df=pd.read_csv('listings.csv')
print(f"Total listings scraped: {len(df)}")
print(f"Failed pages: {len(failed_pages)}")
print(f"Empty pages: {len(empty_pages)}")
print(f"Number of duplicate listing links: {df.duplicated(subset=['listing_link']).sum()}")

df.drop_duplicates(subset=['listing_link'], inplace=True)
df['price']=df['price'].str.replace(r'[^\d.]', '', regex=True).astype(float, errors='ignore')
df['size']=df['size'].str.replace(r'[^\d.]', '', regex=True).astype(float, errors='ignore')
df['bedrooms']=df['bedrooms'].astype(int, errors='ignore')
df['bathrooms']=df['bathrooms'].astype(int, errors='ignore')
df['parking spaces']=df['parking spaces'].astype(int, errors='ignore')
df['location']=df['location'].str.strip().str.title()

df.to_csv('cleaned_listings.csv', index=False)