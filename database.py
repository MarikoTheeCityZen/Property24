import logging
import sqlite3
from sqlite3 import Connection

logger = logging.getLogger(__name__)
db_path="data/listings.db"

def create_connection(db_path: str = db_path) -> Connection:
    try:
        conn = sqlite3.connect(db_path)
        logger.info(f"Connected to database at {db_path}")
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    return conn

def create_table(conn: Connection):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS listings (
        listing_number INTEGER PRIMARY KEY,
        page_number INTEGER,
        title TEXT,
        location TEXT,
        address TEXT,
        description TEXT,
        bedrooms INTEGER,
        bathrooms INTEGER,
        parking_spaces INTEGER,
        size INTEGER,
        price INTEGER,
        listing_link TEXT,
        agency TEXT,
        'SCRAPED_AT' TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error creating table: {e}")

def insert_listing(conn: Connection, listing: dict):
    insert_sql = """
    INSERT OR IGNORE INTO listings (listing_number, page_number, title, location, address, description, bedrooms, bathrooms, parking_spaces, size, price, listing_link, agency)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(insert_sql, (
            listing.get('listing_number'),
            listing.get('page_number'),
            listing.get('title'),
            listing.get('location'),
            listing.get('address'),
            listing.get('description'),
            listing.get('bedrooms'),
            listing.get('bathrooms'),
            listing.get('parking_spaces'),
            listing.get('size'),
            listing.get('price'),
            listing.get('listing_link'),
            listing.get('agency')
        ))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting listing: {e}")