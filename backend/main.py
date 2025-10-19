"""
Furniture Recommendation API.

This module provides the main FastAPI application for furniture recommendations
using semantic search, NLP embeddings, and multi-factor scoring algorithms.

Author: FurniMatch AI Team
Version: 2.0.0
"""

import ssl
from typing import Dict, Any

import numpy as np
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# SSL certificate fix for embedding model downloads
ssl._create_default_https_context = ssl._create_unverified_context

# Configuration and service imports
from config.settings import CORS_ORIGINS, API_HOST, API_PORT
from models.schemas import (
    QueryRequest,
    Product,
    RecommendationResponse,
    AnalyticsResponse,
    ProductListResponse,
)
from utils.data_loader import DataLoader
from utils.helpers import extract_first_image, parse_categories_list
from services.embedding_service import EmbeddingService
from services.recommendation_engine import RecommendationEngine
from services.description_generator import DescriptionGenerator
from services.analytics_service import AnalyticsService

# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

app = FastAPI(
    title="FurniMatch AI Recommendation API",
    description="AI-powered furniture recommendations using NLP and semantic search",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory for the frontend
app.mount("/", StaticFiles(directory="frontend_build", html=True), name="static")


# ============================================================================
# SERVICE INITIALIZATION
# ============================================================================

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Initializing FurniMatch AI Recommendation System")

# Load product data
data_loader = DataLoader()
products_df = data_loader.get_dataframe()

# Initialize embedding service
embedding_service = EmbeddingService()

# Precompute product embeddings for faster similarity search
logger.info("Precomputing product embeddings (this may take a moment)")
product_embeddings = []

for idx, row in products_df.iterrows():
    # Prioritize title and description over metadata
    # Title gets mentioned 3x, description 2x for higher weight
    title = str(row.get("title", ""))
    description = str(row.get("description", ""))
    categories = str(row.get("categories_clean", ""))
    material = str(row.get("material", ""))
    color = str(row.get("color", ""))
    
    # Create weighted text: title appears 3x, description 2x, others 1x
    text_components = [
        title, title, title,  # Title is most important
        description, description,  # Description is second most important
        categories,
        f"{material} {color}" if material or color else ""
    ]
    
    combined_text = " ".join([component for component in text_components if component])
    embedding = embedding_service.encode_text(combined_text)
    product_embeddings.append(embedding)

product_embeddings = np.array(product_embeddings)
logger.info(f"Computed embeddings for {len(products_df):,} products")

# Initialize recommendation engine with embeddings
recommendation_engine = RecommendationEngine(products_df, product_embeddings)

# Initialize analytics service
analytics_service = AnalyticsService(products_df)

logger.info("FurniMatch AI System Ready")
logger.info(f"Loaded {len(products_df):,} products")

# ============================================================================
# API ENDPOINTS
# ============================================================================


@app.get("/", tags=["Health"])
def root() -> Dict[str, Any]:
    """
    API root endpoint with system information.
    
    Returns:
        System status and available endpoints
    """
    return {
        "name": "FurniMatch AI API",
        "version": "2.0.0",
        "status": "operational",
        "total_products": len(products_df),
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "recommend": "POST /recommend",
            "analytics": "GET /analytics",
            "products": "GET /products",
            "product_detail": "GET /product/{product_id}",
        },
    }


@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring.
    
    Returns:
        Health status
    """
    return {"status": "healthy", "service": "furnimatch-api"}


@app.post("/recommend", response_model=RecommendationResponse, tags=["Recommendations"])
async def get_recommendations(request: QueryRequest) -> RecommendationResponse:
    """
    Get personalized furniture recommendations based on a text query.
    
    This endpoint uses advanced multi-factor scoring algorithm:
    - Text semantic similarity (70%): Matches query meaning with product descriptions
    - Category matching (15%): Prioritizes relevant furniture categories
    - Material matching (8%): Considers material preferences
    - Color matching (7%): Accounts for color preferences
    
    Args:
        request: Query request containing search text, filters, and parameters
    
    Returns:
        Recommended products with generated description
    
    Raises:
        HTTPException: If recommendation generation fails
    """
    try:
        # Log incoming request
        if request.filters:
            logger.info(f"Query: '{request.query}' with filters: {request.filters}")
        else:
            logger.info(f"Query: '{request.query}' (no filters)")

        # Generate query embedding
        query_embedding = embedding_service.encode_text(request.query)

        # Search for similar products
        similar_products = recommendation_engine.search(
            query_embedding=query_embedding,
            query_text=request.query,
            top_k=request.top_k,
            filters=request.filters,
        )

        # Generate natural language description
        description = DescriptionGenerator.generate(similar_products, request.query)

        # Format products for API response
        formatted_products = []
        for product in similar_products:
            formatted_products.append(
                Product(
                    uniq_id=str(product.get("uniq_id", "")),
                    title=product.get("title", ""),
                    brand=product.get("brand", ""),
                    description=product.get("description", ""),
                    price=float(product.get("price", 0)),
                    categories=parse_categories_list(product.get("categories", "")),
                    images=extract_first_image(product.get("images", "")),
                    color=product.get("color", ""),
                    material=product.get("material", ""),
                    manufacturer=product.get("manufacturer"),
                    country_of_origin=product.get("country_of_origin"),
                    similarity_score=product.get("similarity_score"),
                )
            )

        return RecommendationResponse(
            products=formatted_products,
            generated_description=description,
            query_embedding=query_embedding.tolist(),
            total_matches=len(formatted_products),
        )

    except Exception as e:
        logger.error(f"Error in recommendations: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Recommendation error: {str(e)}"
        )


@app.get("/analytics", response_model=AnalyticsResponse, tags=["Analytics"])
async def get_analytics() -> AnalyticsResponse:
    """
    Get comprehensive analytics about the product catalog.
    
    Returns:
        Analytics data including price distributions, category breakdowns,
        top brands, and material distributions
    
    Raises:
        HTTPException: If analytics generation fails
    """
    try:
        analytics_data = analytics_service.get_analytics()

        return AnalyticsResponse(
            total_products=analytics_data["total_products"],
            avg_price=analytics_data["avg_price"],
            price_distribution=analytics_data["price_distribution"],
            category_breakdown=analytics_data["category_breakdown"],
            top_brands=analytics_data["top_brands"],
            material_distribution=analytics_data["material_distribution"],
        )

    except Exception as e:
        logger.error(f"Error in analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")


@app.get("/products", response_model=ProductListResponse, tags=["Products"])
async def get_all_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum products to return"),
) -> ProductListResponse:
    """
    Get paginated list of all products in the catalog.
    
    Args:
        skip: Number of products to skip for pagination
        limit: Maximum number of products to return (capped at 100)
    
    Returns:
        Paginated product list with metadata
    
    Raises:
        HTTPException: If product fetching fails
    """
    try:
        products = products_df.iloc[skip : skip + limit].to_dict("records")

        return ProductListResponse(
            total=len(products_df),
            skip=skip,
            limit=limit,
            products=products,
        )

    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching products: {str(e)}"
        )


@app.get("/product/{product_id}", tags=["Products"])
async def get_product(product_id: str) -> Dict[str, Any]:
    """
    Get specific product details by ID.
    
    Args:
        product_id: Unique product identifier
    
    Returns:
        Product details dictionary
    
    Raises:
        HTTPException: If product not found or fetch fails
    """
    try:
        product = data_loader.get_product_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID '{product_id}' not found",
            )

        return product

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching product: {str(e)}"
        )


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 80)
    logger.info(f"Starting FurniMatch AI API Server")
    logger.info(f"Host: {API_HOST}:{API_PORT}")
    logger.info(f"API Documentation: http://{API_HOST}:{API_PORT}/api/docs")
    logger.info("=" * 80)

    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info",
        access_log=True,
    )

