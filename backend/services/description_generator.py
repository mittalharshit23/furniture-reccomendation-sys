"""Description generation service using templates."""
from typing import List, Dict


class DescriptionGenerator:
    """Generates natural language descriptions for recommendations."""
    
    @staticmethod
    def generate(products: List[Dict], query: str) -> str:
        """
        Generate a helpful description for the recommended products.
        
        Args:
            products: List of recommended products
            query: Original user query
        
        Returns:
            Natural language description
        """
        if not products:
            return "We couldn't find exact matches for your search. Try different keywords or adjust your filters."
        
        num_products = len(products)
        top_product = products[0]
        
        # Extract common features
        materials = list(set([p.get('material', '').lower() for p in products[:3] if p.get('material')]))
        categories = DescriptionGenerator._extract_main_category(products)
        
        # Build description
        description_parts = []
        
        # Opening
        if num_products == 1:
            description_parts.append(f"Found 1 great match for '{query}'.")
        else:
            description_parts.append(f"Found {num_products} excellent matches for '{query}'.")
        
        # Highlight top result
        if top_product.get('similarity_score', 0) > 0.6:
            description_parts.append(
                f"Our top recommendation is the {top_product.get('title', 'featured item')} "
                f"by {top_product.get('brand', 'a quality brand')}."
            )
        
        # Material info
        if materials and materials[0]:
            materials_clean = [m for m in materials if m and len(m) > 2][:2]
            if materials_clean:
                mat_str = ' and '.join(materials_clean)
                description_parts.append(f"These pieces feature {mat_str} construction.")
        
        # Category context
        if categories:
            description_parts.append(f"Perfect for your {categories} needs.")
        
        return ' '.join(description_parts)
    
    @staticmethod
    def _extract_main_category(products: List[Dict]) -> str:
        """Extract the main category from products."""
        categories = []
        for p in products[:3]:
            cat_str = str(p.get('categories_clean', ''))
            if cat_str:
                # Get first category
                first_cat = cat_str.split(',')[0].strip()
                categories.append(first_cat.lower())
        
        if not categories:
            return ''
        
        # Return most common category
        from collections import Counter
        most_common = Counter(categories).most_common(1)
        return most_common[0][0] if most_common else ''
