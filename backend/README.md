# Furniture Recommendation System - Backend

## 🎯 Version 2.0 - Clean Architecture with Precision Recommendations

### Overview
AI-powered furniture recommendation system using advanced NLP, semantic search, and multi-factor scoring for precise results.

### Key Improvements in V2.0
- ✅ **Clean, modular architecture** - Organized into services, models, utils, and config
- ✅ **Precision-focused recommendations** - Multi-factor scoring algorithm
- ✅ **Better code organization** - Separated concerns, reusable components
- ✅ **Improved matching** - Category, material, and color-aware search
- ✅ **Configurable thresholds** - Minimum similarity filtering for quality results

### Architecture

```
backend/
├── config/
│   └── settings.py          # Central configuration
├── models/
│   └── schemas.py            # Pydantic models for API
├── services/
│   ├── embedding_service.py  # Text/image embedding generation
│   ├── recommendation_engine.py  # Multi-factor recommendation algorithm
│   ├── description_generator.py  # Natural language descriptions
│   └── analytics_service.py  # Analytics dashboard data
├── utils/
│   ├── data_loader.py        # Data loading and preprocessing
│   └── helpers.py            # Utility functions
├── data/
│   └── furniture_dataset.csv # Product catalog
├── main.py                   # FastAPI application
└── .env                      # Environment variables
```

### Multi-Factor Recommendation Algorithm

The system uses weighted scoring across multiple dimensions:

1. **Text Semantic Similarity (70%)** - Primary matching using sentence embeddings
2. **Category Matching (15%)** - Keyword-based category alignment
3. **Material Matching (8%)** - Specific material requests (wood, metal, etc.)
4. **Color Matching (7%)** - Color preferences in query

**Minimum Threshold:** 0.3 cosine similarity (configurable in `config/settings.py`)

### Features

- 🎯 **Precise Recommendations** - Returns fewer but highly relevant results
- 🔍 **Semantic Search** - Understands natural language queries
- 🏷️ **Smart Filtering** - Price, category, material, and color filters
- 📊 **Analytics Dashboard** - Product catalog insights
- 🚀 **Fast Performance** - Precomputed embeddings for instant search
- 🌐 **Network Ready** - Configured for LAN access

### API Endpoints

#### 1. Get Recommendations
```http
POST /recommend
Content-Type: application/json

{
  "query": "modern black office chair",
  "top_k": 5,
  "filters": {
    "max_price": 200,
    "min_price": 50,
    "material": "leather",
    "color": "black"
  }
}
```

**Response includes:**
- Matched products with similarity scores
- Natural language description
- Query embedding for analysis

#### 2. Analytics Dashboard
```http
GET /analytics
```

Returns:
- Total products
- Price distribution
- Category breakdown
- Top brands
- Material distribution

#### 3. Product Listing
```http
GET /products?skip=0&limit=50
```

#### 4. Single Product
```http
GET /product/{product_id}
```

#### 5. Health Check
```http
GET /health
```

### Configuration

Edit `backend/.env`:

```env
# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database
DATABASE_PATH=data/furniture_dataset.csv

# Recommendation Settings (in config/settings.py)
MIN_SIMILARITY_THRESHOLD=0.3  # Precision control
DEFAULT_TOP_K=5
SIMILARITY_WEIGHTS={
    "text": 0.7,
    "category": 0.15,
    "material": 0.08,
    "color": 0.07
}
```

### Running the Server

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python3 main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Network Access

Backend accessible at:
- Local: `http://localhost:8000`
- Network: `http://192.168.29.186:8000`

Frontend configured to use network IP for multi-user access.

### Testing

```bash
# Test health
curl http://localhost:8000/health

# Test recommendation
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "comfortable office chair", "top_k": 3}'

# Test analytics
curl http://localhost:8000/analytics
```

### Dependencies

- **FastAPI** - Web framework
- **Sentence Transformers** - Text embeddings
- **PyTorch + TorchVision** - Image processing
- **Pandas** - Data handling
- **scikit-learn** - Similarity calculations
- **Pydantic** - Data validation
- **python-dotenv** - Environment management

### Performance

- **Initial Load:** ~8-10 seconds (embedding computation)
- **Query Time:** <100ms (precomputed embeddings)
- **Products:** 215 items with full metadata
- **Embedding Dimension:** 384 (MiniLM-L6-v2)

### Code Quality

- ✅ Modular design
- ✅ Type hints
- ✅ Comprehensive docstrings
- ✅ Error handling
- ✅ Logging
- ✅ Configuration management

### Future Enhancements

- [ ] Vector database integration (Pinecone/Weaviate)
- [ ] Image-based search
- [ ] User preference learning
- [ ] A/B testing for scoring weights
- [ ] Caching layer for popular queries
- [ ] Batch recommendation API

### License

MIT

### Authors

Built with ❤️ for precise furniture recommendations
