"""
Dataset inspection utility.

This script provides comprehensive analysis of the furniture dataset including
shape, columns, data types, missing values, and basic statistics.
"""

import sys
from pathlib import Path

import pandas as pd

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import DATABASE_PATH


def inspect_dataset(csv_path: str = DATABASE_PATH) -> None:
    """
    Inspect and display comprehensive information about the dataset.
    
    Args:
        csv_path: Path to the CSV file to inspect
    """
    try:
        df = pd.read_csv(csv_path)
        
        print("=" * 80)
        print("DATASET INSPECTION REPORT")
        print("=" * 80)
        
        print(f"\nFile: {csv_path}")
        print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
        print(f"\nColumns ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        print(f"\nFirst 5 Rows:")
        print(df.head().to_string())
        
        print(f"\nData Types:")
        print(df.dtypes.to_string())
        
        print(f"\nMissing Values:")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        missing_df = pd.DataFrame({
            'Missing Count': missing,
            'Percentage': missing_pct
        })
        print(missing_df[missing_df['Missing Count'] > 0].to_string())
        
        print(f"\nNumeric Columns Statistics:")
        print(df.describe().to_string())
        
        print("\n" + "=" * 80)
        print("Inspection Complete")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"ERROR: File not found at {csv_path}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: during inspection: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_dataset(sys.argv[1])
    else:
        inspect_dataset()
