"""
Dataset mapping utility.

This script maps custom dataset columns to the expected format required by the
recommendation system. Modify the column mapping based on your CSV structure.
"""

import sys
from pathlib import Path
from typing import Dict

import pandas as pd

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


def create_column_mapping() -> Dict[str, str]:
    """
    Define column mapping from source dataset to expected format.
    
    Modify this mapping based on your actual CSV column names.
    
    Returns:
        Dictionary mapping source column names to target column names
    """
    return {
        # Source column name: Target column name
        'product_name': 'title',
        'brand_name': 'brand',
        'product_description': 'description',
        'product_price': 'price',
        'category': 'categories',
        'image_url': 'images',
        'product_material': 'material',
        'product_color': 'color',
        'id': 'uniq_id',
        'manufacturer_name': 'manufacturer',
        'origin_country': 'country_of_origin'
    }


def map_dataset(
    input_path: str,
    output_path: str,
    column_mapping: Dict[str, str] = None
) -> None:
    """
    Map dataset columns to expected format and clean data.
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to save processed CSV file
        column_mapping: Optional custom column mapping
    """
    try:
        print(f"Loading dataset from: {input_path}")
        df = pd.read_csv(input_path)
        original_shape = df.shape
        
        # Apply column mapping
        if column_mapping is None:
            column_mapping = create_column_mapping()
        
        # Only rename columns that exist in the dataframe
        existing_mappings = {
            src: tgt for src, tgt in column_mapping.items()
            if src in df.columns
        }
        
        if existing_mappings:
            df = df.rename(columns=existing_mappings)
            print(f"INFO: Renamed {len(existing_mappings)} columns")
        
        # Handle missing values with appropriate defaults
        default_values = {
            'description': '',
            'brand': 'Unknown',
            'material': 'Mixed',
            'color': 'Multicolor',
            'manufacturer': '',
            'country_of_origin': ''
        }
        
        for col, default in default_values.items():
            if col in df.columns:
                df[col] = df[col].fillna(default)
        
        # Clean and standardize price column
        if 'price' in df.columns:
            df['price'] = df['price'].astype(str).str.replace('[$,]', '', regex=True)
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            before_drop = len(df)
            df = df.dropna(subset=['price'])
            dropped = before_drop - len(df)
            if dropped > 0:
                print(f"Warning: Dropped {dropped} rows with invalid prices")
        
        # Create uniq_id if not exists
        if 'uniq_id' not in df.columns:
            df['uniq_id'] = df.index.astype(str)
            print("INFO: Generated unique IDs")
        
        # Remove duplicates
        before_dedup = len(df)
        df = df.drop_duplicates(subset=['uniq_id'], keep='first')
        deduped = before_dedup - len(df)
        if deduped > 0:
            print(f"INFO: Removed {deduped} duplicate rows")
        
        # Save processed dataset
        df.to_csv(output_path, index=False)
        
        print(f"\nSUCCESS: Dataset processed successfully!")
        print(f"   Original: {original_shape[0]:,} rows × {original_shape[1]} columns")
        print(f"   Final: {len(df):,} rows × {len(df.columns)} columns")
        print(f"   Saved to: {output_path}")
        
    except FileNotFoundError:
        print(f"ERROR: Input file not found at {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        input_file = "data/furniture_dataset.csv"
        output_file = "data/processed_furniture_data.csv"
    
    print("Dataset Mapper")
    print("=" * 80)
    map_dataset(input_file, output_file)
