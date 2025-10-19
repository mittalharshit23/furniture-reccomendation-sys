"""Data loading and preprocessing utilities."""
import logging
from typing import Tuple

import pandas as pd
import numpy as np

from config.settings import DATABASE_PATH

logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading and preprocessing of furniture dataset."""
    
    def __init__(self):
        self.df = None
        self.load_data()
    
    def load_data(self) -> pd.DataFrame:
        """Load and preprocess the furniture dataset."""
        logger.info(f" Loading dataset from {DATABASE_PATH}...")
        
        self.df = pd.read_csv(DATABASE_PATH)
        
        # Remove duplicate products based on uniq_id
        original_count = len(self.df)
        self.df = self.df.drop_duplicates(subset=['uniq_id'], keep='first')
        duplicates_removed = original_count - len(self.df)
        if duplicates_removed > 0:
            logger.info(f" Removed {duplicates_removed} duplicate products")
        
        # Clean price column
        if 'price' in self.df.columns:
            self.df['price'] = self.df['price'].astype(str).str.replace('$', '').str.replace(',', '')
            self.df['price'] = pd.to_numeric(self.df['price'], errors='coerce')
            self.df = self.df.dropna(subset=['price'])
        
        # Fill NaN values for optional fields
        self.df = self.df.fillna({
            'manufacturer': '',
            'country_of_origin': '',
            'material': '',
            'color': '',
            'description': '',
            'brand': 'Unknown',
            'categories': '',
            'images': '',
            'title': ''
        })
        
        # Clean and standardize text fields
        self.df['material'] = self.df['material'].str.lower().str.strip()
        self.df['color'] = self.df['color'].str.lower().str.strip()
        
        # Parse categories if stored as string representation of list
        self.df['categories_clean'] = self.df['categories'].apply(self._parse_categories)
        
        # Reset index after cleaning
        self.df = self.df.reset_index(drop=True)
        
        logger.info(f" Loaded {len(self.df)} unique products")
        return self.df
    
    @staticmethod
    def _parse_categories(cat_str: str) -> str:
        """Parse category string and extract main categories."""
        if not cat_str or cat_str == '':
            return ''
        
        # Remove list brackets and quotes
        cat_str = str(cat_str).replace('[', '').replace(']', '').replace("'", "").replace('"', '')
        
        # Split by comma and get first 3 categories (most relevant)
        categories = [c.strip() for c in cat_str.split(',')][:3]
        return ', '.join(categories)
    
    def get_dataframe(self) -> pd.DataFrame:
        """Return the loaded dataframe."""
        return self.df
    
    def get_product_by_id(self, product_id: str) -> dict:
        """Get a specific product by ID."""
        product = self.df[self.df['uniq_id'] == product_id]
        if product.empty:
            return None
        return product.iloc[0].to_dict()
