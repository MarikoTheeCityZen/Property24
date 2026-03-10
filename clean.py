import re
def clean_price(price):
    if price is None:
        return None
    price = re.sub(r'[^\d.]', '', price)
    try:
        return float(price)
    except ValueError:
        return None
def clean_bedrooms(bedrooms):
    if bedrooms is None:
        return None
    match = re.search(r'(\d+)', bedrooms)
    return int(match.group(1)) if match else None

def clean_bathrooms(bathrooms):
    if bathrooms is None:
        return None
    match = re.search(r'(\d+)', bathrooms)
    return int(match.group(1)) if match else None

def clean_parking_spaces(parking_spaces):
    if parking_spaces is None:
        return None
    match = re.search(r'(\d+)', parking_spaces)
    return int(match.group(1)) if match else None
def clean_size(size):
    if size is None:
        return None
    match = re.search(r'(\d+)', size)
    return int(match.group(1)) if match else None