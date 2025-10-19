"""
Analytics service for product catalog insights.

This module provides comprehensive analytics about the furniture catalog
including price distributions, category breakdowns, and brand statistics.
"""

from typing import Dict, List

import pandas as pd


class AnalyticsService:
    """
    Service for generating product catalog analytics.
    
    Provides methods to compute statistics, distributions, and insights
    about the furniture product catalog for dashboard visualization.
    """

    def __init__(self, products_df: pd.DataFrame):
        """
        Initialize analytics service with product data.
        
        Args:
            products_df: DataFrame containing product information
        """
        self.df = products_df

    def get_analytics(self) -> Dict:
        """
        Generate comprehensive analytics data for the dashboard.
        
        Returns:
            Dictionary containing:
                - total_products: Total number of products
                - avg_price: Average product price
                - price_distribution: Products grouped by price range
                - category_breakdown: Top product categories
                - top_brands: Most represented brands
                - material_distribution: Products by material type
        """
        # Calculate basic statistics
        total_products = len(self.df)
        avg_price = float(self.df["price"].mean())

        # Compute price distribution across ranges
        price_dist = self._get_price_distribution()

        # Analyze category breakdown
        category_dist = self._get_category_breakdown()

        # Get top brands
        top_brands_list = self._get_top_brands(limit=10)

        # Analyze material distribution
        material_dist = self._get_material_distribution(limit=10)

        return {
            "total_products": total_products,
            "avg_price": round(avg_price, 2),
            "price_distribution": price_dist,
            "category_breakdown": category_dist,
            "top_brands": top_brands_list,
            "material_distribution": material_dist,
        }

    def _get_price_distribution(self) -> Dict[str, int]:
        """
        Group products into price ranges.
        
        Returns:
            Dictionary mapping price ranges to product counts
        """
        price_bins = [0, 50, 100, 200, 500, 1000, float("inf")]
        price_labels = ["$0-50", "$50-100", "$100-200", "$200-500", "$500-1000", "$1000+"]

        price_ranges = pd.cut(self.df["price"], bins=price_bins, labels=price_labels)
        price_counts = price_ranges.value_counts()

        # Convert to string keys for JSON serialization
        return {str(k): int(v) for k, v in price_counts.items()}

    def _get_category_breakdown(self, limit: int = 10) -> Dict[str, int]:
        """
        Get distribution of products across top categories.
        
        Args:
            limit: Maximum number of categories to return
        
        Returns:
            Dictionary mapping categories to product counts
        """
        all_categories = []

        for cat_str in self.df["categories_clean"]:
            if cat_str and str(cat_str).strip():
                # Extract first (primary) category
                primary_category = str(cat_str).split(",")[0].strip()
                all_categories.append(primary_category)

        # Count and get top categories
        category_counts = pd.Series(all_categories).value_counts().head(limit)

        return {str(k): int(v) for k, v in category_counts.items()}

    def _get_top_brands(self, limit: int = 10) -> List[Dict[str, any]]:
        """
        Get most represented brands in the catalog.
        
        Args:
            limit: Maximum number of brands to return
        
        Returns:
            List of dictionaries with brand name and product count
        """
        top_brands = self.df["brand"].value_counts().head(limit).reset_index()
        top_brands.columns = ["brand", "count"]

        return [
            {"brand": row["brand"], "count": int(row["count"])}
            for _, row in top_brands.iterrows()
        ]

    def _get_material_distribution(self, limit: int = 10) -> Dict[str, int]:
        """
        Get distribution of products by material type.
        
        Args:
            limit: Maximum number of materials to return
        
        Returns:
            Dictionary mapping materials to product counts
        """
        material_counts = self.df["material"].value_counts().head(limit)

        # Filter out empty or invalid materials
        return {
            str(k): int(v)
            for k, v in material_counts.items()
            if k and str(k).strip()
        }

