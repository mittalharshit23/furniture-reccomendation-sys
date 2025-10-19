"""Advanced recommendation engine with multi-factor scoring."""
import logging
from typing import List, Dict, Optional

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from config.settings import (
    MIN_SIMILARITY_THRESHOLD, 
    MAX_RESULTS, 
    SIMILARITY_WEIGHTS
)

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Advanced recommendation engine using multi-factor scoring:
    1. Text semantic similarity (primary)
    2. Category matching (secondary)
    3. Material matching (tertiary)
    4. Color matching (quaternary)
    """
    
    def __init__(self, products_df: pd.DataFrame, product_embeddings: np.ndarray):
        self.products_df = products_df
        self.product_embeddings = product_embeddings
        logger.info(f" Recommendation engine initialized with {len(products_df)} products")
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        query_text: str,
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar products using multi-factor scoring.
        
        Args:
            query_embedding: Embedding vector of the query
            query_text: Original query text for keyword matching
            top_k: Number of results to return
            filters: Optional filters (price, category, material, color)
        
        Returns:
            List of unique products with similarity scores
        """
        # Step 1: Calculate text similarity scores
        query_emb = np.array(query_embedding).reshape(1, -1)
        text_similarities = cosine_similarity(query_emb, self.product_embeddings)[0]
        
        # Step 2: Calculate category, material, and color bonus scores
        category_scores = self._calculate_category_scores(query_text)
        material_scores = self._calculate_material_scores(query_text)
        color_scores = self._calculate_color_scores(query_text)
        
        # Step 3: Combine scores with weights
        # If no keyword matches found, rely purely on text similarity
        has_keywords = (category_scores.sum() > 0 or 
                       material_scores.sum() > 0 or 
                       color_scores.sum() > 0)
        
        if has_keywords:
            combined_scores = (
                SIMILARITY_WEIGHTS["text"] * text_similarities +
                SIMILARITY_WEIGHTS["category"] * category_scores +
                SIMILARITY_WEIGHTS["material"] * material_scores +
                SIMILARITY_WEIGHTS["color"] * color_scores
            )
        else:
            # No keywords matched - use pure text similarity
            combined_scores = text_similarities
        
        # Step 4: Filter by minimum threshold
        valid_indices = np.where(combined_scores >= MIN_SIMILARITY_THRESHOLD)[0]
        
        if len(valid_indices) == 0:
            # Lower threshold slightly if no results
            valid_indices = np.where(combined_scores >= MIN_SIMILARITY_THRESHOLD * 0.85)[0]
        
        if len(valid_indices) == 0:
            # Still no results - return top matches anyway but with warning
            valid_indices = np.argsort(combined_scores)[::-1][:top_k * 2]
            logger.warning(f"No results met similarity threshold for query: '{query_text}'")
        
        # Step 5: Sort by combined score
        sorted_indices = valid_indices[np.argsort(combined_scores[valid_indices])[::-1]]
        
        # Step 6: Get top products before filtering (get extra for deduplication)
        top_indices = sorted_indices[:top_k * 3]
        similar_products = []
        seen_ids = set()
        
        for idx in top_indices:
            product = self.products_df.iloc[idx].to_dict()
            product_id = product.get('uniq_id', '')
            
            if product_id in seen_ids:
                continue
            
            seen_ids.add(product_id)
            product['similarity_score'] = float(combined_scores[idx])
            product['text_similarity'] = float(text_similarities[idx])
            similar_products.append(product)
            
            if len(similar_products) >= top_k * 2:
                break
        
        # Step 7: Apply filters
        if filters:
            similar_products = self._apply_filters(similar_products, filters)
        
        # Step 8: Return top_k unique results
        return similar_products[:top_k]
    
    def _calculate_category_scores(self, query_text: str) -> np.ndarray:
        """Calculate category matching scores based on keyword overlap."""
        query_lower = query_text.lower()
        scores = np.zeros(len(self.products_df))
        
        # Common furniture category keywords - expanded list
        category_keywords = {
            'chair': ['chair', 'seat', 'stool', 'seating'],
            'table': ['table', 'desk', 'console', 'stand'],
            'bed': ['bed', 'mattress', 'bedroom', 'headboard', 'frame'],
            'sofa': ['sofa', 'couch', 'loveseat', 'sectional', 'futon'],
            'storage': ['storage', 'cabinet', 'shelf', 'shelving', 'organizer', 'rack', 'drawer', 'dresser', 'chest'],
            'outdoor': ['outdoor', 'patio', 'garden', 'deck'],
            'office': ['office', 'desk', 'workspace', 'workstation'],
            'kitchen': ['kitchen', 'dining', 'pantry'],
            'lighting': ['lamp', 'light', 'lighting', 'fixture', 'chandelier', 'sconce'],
            'bathroom': ['bathroom', 'bath', 'shower', 'vanity', 'toilet'],
            'living': ['living', 'room', 'family'],
            'bookshelf': ['bookshelf', 'bookcase', 'shelving'],
            'nightstand': ['nightstand', 'bedside', 'night table'],
            'ottoman': ['ottoman', 'footstool', 'pouf'],
            'bench': ['bench', 'seating bench'],
            'wardrobe': ['wardrobe', 'armoire', 'closet'],
            'mirror': ['mirror', 'wall mirror'],
            'rug': ['rug', 'carpet', 'mat'],
        }
        
        # Find which categories match the query
        matched_keywords = []
        for cat, keywords in category_keywords.items():
            if any(kw in query_lower for kw in keywords):
                matched_keywords.extend(keywords)
        
        if not matched_keywords:
            return scores
        
        # Score products based on category overlap
        for i in range(len(self.products_df)):
            row = self.products_df.iloc[i]
            categories = str(row.get('categories_clean', '')).lower()
            title = str(row.get('title', '')).lower()
            description = str(row.get('description', '')).lower()
            
            # Count keyword matches in categories, title, and description
            matches_in_categories = sum(1 for kw in matched_keywords if kw in categories)
            matches_in_title = sum(1 for kw in matched_keywords if kw in title)
            matches_in_description = sum(1 for kw in matched_keywords if kw in description)
            
            # Weighted scoring: title > categories > description
            total_matches = (matches_in_title * 2.0 + 
                           matches_in_categories * 1.5 + 
                           matches_in_description * 1.0)
            
            # Normalize by max possible score
            max_possible = len(matched_keywords) * 2.0
            scores[i] = min(total_matches / max_possible, 1.0)
        
        return scores
    
    def _calculate_material_scores(self, query_text: str) -> np.ndarray:
        """Calculate material matching scores."""
        query_lower = query_text.lower()
        scores = np.zeros(len(self.products_df))
        
        # Material keywords - expanded
        materials = ['wood', 'wooden', 'oak', 'pine', 'walnut', 'mahogany',
                    'metal', 'steel', 'iron', 'aluminum', 'brass',
                    'plastic', 'acrylic', 'resin',
                    'fabric', 'upholstered', 'textile', 'linen', 'velvet',
                    'leather', 'faux leather', 'genuine leather',
                    'glass', 'tempered glass',
                    'bamboo', 'wicker', 'rattan', 'cane',
                    'marble', 'stone', 'concrete',
                    'foam', 'cushion', 'padded']
        
        matched_materials = [m for m in materials if m in query_lower]
        
        if not matched_materials:
            return scores
        
        for i in range(len(self.products_df)):
            row = self.products_df.iloc[i]
            material = str(row.get('material', '')).lower()
            title = str(row.get('title', '')).lower()
            
            # Check if any matched material is in product material or title
            if any(m in material or m in title for m in matched_materials):
                scores[i] = 1.0
        
        return scores
    
    def _calculate_color_scores(self, query_text: str) -> np.ndarray:
        """Calculate color matching scores."""
        query_lower = query_text.lower()
        scores = np.zeros(len(self.products_df))
        
        # Color keywords - expanded
        colors = ['black', 'white', 'brown', 'gray', 'grey', 'beige', 'tan', 'cream', 'ivory',
                 'blue', 'navy', 'light blue', 'dark blue',
                 'red', 'burgundy', 'maroon',
                 'green', 'olive', 'sage',
                 'yellow', 'gold', 'mustard',
                 'orange', 'rust', 'coral',
                 'pink', 'rose', 'blush',
                 'purple', 'lavender', 'plum',
                 'silver', 'bronze', 'copper']
        
        matched_colors = [c for c in colors if c in query_lower]
        
        if not matched_colors:
            return scores
        
        for i in range(len(self.products_df)):
            row = self.products_df.iloc[i]
            color = str(row.get('color', '')).lower()
            title = str(row.get('title', '')).lower()
            
            # Check if any matched color is in product color or title
            if any(c in color or c in title for c in matched_colors):
                scores[i] = 1.0
        
        return scores
    
    def _apply_filters(self, products: List[Dict], filters: Dict) -> List[Dict]:
        """Apply price, category, material, and color filters."""
        filtered = products
        initial_count = len(filtered)
        
        if 'max_price' in filters:
            before = len(filtered)
            filtered = [p for p in filtered if float(p.get('price', 0)) <= filters['max_price']]
            logger.debug(f"   Max price ${filters['max_price']}: {before} → {len(filtered)} products")
        
        if 'min_price' in filters:
            before = len(filtered)
            filtered = [p for p in filtered if float(p.get('price', 0)) >= filters['min_price']]
            logger.debug(f"   Min price ${filters['min_price']}: {before} → {len(filtered)} products")
        
        if 'categories' in filters:
            before = len(filtered)
            cat_list = filters['categories'] if isinstance(filters['categories'], list) else [filters['categories']]
            filtered = [
                p for p in filtered 
                if any(cat.lower() in str(p.get('categories', '')).lower() for cat in cat_list)
            ]
            logger.debug(f"   Categories {cat_list}: {before} → {len(filtered)} products")
        
        if 'material' in filters:
            before = len(filtered)
            material_filter = filters['material'].lower()
            filtered = [
                p for p in filtered 
                if material_filter in str(p.get('material', '')).lower()
            ]
            logger.debug(f"   Material '{material_filter}': {before} → {len(filtered)} products")
        
        if 'color' in filters:
            before = len(filtered)
            color_filter = filters['color'].lower()
            filtered = [
                p for p in filtered 
                if color_filter in str(p.get('color', '')).lower()
            ]
            logger.debug(f"   Color '{color_filter}': {before} → {len(filtered)} products")
        
        if initial_count != len(filtered):
            logger.info(f" Filters applied: {initial_count} → {len(filtered)} products remaining")
        
        return filtered
