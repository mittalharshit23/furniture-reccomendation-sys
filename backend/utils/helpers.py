"""Utility functions for the application."""
import re
from typing import List


def extract_first_image(image_str: str) -> str:
    """
    Extract first valid image URL from string.
    
    Args:
        image_str: String containing image URL(s)
    
    Returns:
        First valid image URL or empty string
    """
    if not image_str or image_str == '':
        return ''
    
    # If it's a string representation of a list like "['url1', 'url2']"
    if isinstance(image_str, str) and image_str.startswith('['):
        # Extract URLs from the string
        urls = re.findall(r'https?://[^\s\'"]+', image_str)
        if urls:
            # Return first URL, cleaned
            return urls[0].strip().rstrip(',')
    
    # If it's just a URL string
    if isinstance(image_str, str) and image_str.startswith('http'):
        return image_str.strip()
    
    return ''


def parse_categories_list(cat_str: str) -> List[str]:
    """
    Parse category string into list.
    
    Args:
        cat_str: String representation of categories
    
    Returns:
        List of category strings
    """
    if not cat_str or cat_str == '':
        return []
    
    # Remove brackets and quotes
    cat_str = str(cat_str).replace('[', '').replace(']', '').replace("'", "").replace('"', '')
    
    # Split by comma and clean
    categories = [c.strip() for c in cat_str.split(',') if c.strip()]
    return categories


def format_price(price: float) -> str:
    """Format price as currency string."""
    return f"${price:,.2f}"
