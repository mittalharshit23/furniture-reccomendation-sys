"""Pydantic models for API request/response validation."""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for furniture recommendations."""
    query: str = Field(..., min_length=1, description="User search query")
    top_k: int = Field(default=5, ge=1, le=10, description="Number of results to return")
    filters: Optional[Dict] = Field(default=None, description="Optional filters (price, category, material, color)")


class Product(BaseModel):
    """Product model for API responses."""
    uniq_id: str
    title: str
    brand: str
    description: str
    price: float
    categories: List[str]
    images: str
    color: str
    material: str
    manufacturer: Optional[str] = None
    country_of_origin: Optional[str] = None
    similarity_score: Optional[float] = None


class RecommendationResponse(BaseModel):
    """Response model for recommendations."""
    products: List[Product]
    generated_description: str
    query_embedding: List[float]
    total_matches: int


class AnalyticsResponse(BaseModel):
    """Response model for analytics dashboard."""
    total_products: int
    avg_price: float
    price_distribution: Dict
    category_breakdown: Dict
    top_brands: List[Dict]
    material_distribution: Dict


class ProductListResponse(BaseModel):
    """Response model for paginated product list."""
    total: int
    skip: int
    limit: int
    products: List[Dict]
