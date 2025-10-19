# FurniMatch AI - Intelligent Furniture Recommendation System

**Version:** 2.0.0  
**Python:** 3.12+  
**React:** 19.2.0  
**Framework:** FastAPI

An AI-powered furniture recommendation system using semantic search, natural language processing, and multi-factor scoring algorithms.

## Features

- Semantic Search: Natural language queries for furniture discovery
- Multi-Factor Scoring: Text similarity (70%), category (15%), material (8%), color (7%)
- Advanced Filters: Price range, category, material, and color filtering
- Real-time Analytics: Comprehensive product catalog insights
- Responsive Design: Mobile-friendly interface with TailwindCSS
- REST API: Well-documented API with OpenAPI/Swagger docs

## Project Structure

```
furniture-recommendation-system/
├── backend/                 # Python FastAPI backend
│   ├── config/             # Configuration management
│   ├── models/             # Pydantic schemas
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   ├── scripts/            # Data processing tools
│   └── main.py             # Application entry point
├── frontend/               # React frontend
│   └── src/
│       ├── services/       # API integration
│       ├── utils/          # Helper functions
│       ├── constants/      # Configuration
│       └── App.js          # Main component
└── docker-compose.yml      # Container orchestration
```

## Quick Start

### Using Docker (Recommended)

```bash
cd furniture-recommendation-system
docker compose up --build
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Local Development

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm start
```

## Dataset Format

Required CSV columns:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| uniq_id | string | Yes | Unique identifier |
| title | string | Yes | Product name |
| brand | string | Yes | Brand name |
| price | float | Yes | Product price |
| categories | string | Yes | Categories (comma-separated) |
| description | string | No | Product description |
| images | string | No | Image URL |
| material | string | No | Primary material |
| color | string | No | Primary color |

### Custom Dataset Mapping

```bash
python backend/scripts/dataset_inspector.py data/your_dataset.csv
python backend/scripts/dataset_mapper.py data/your_dataset.csv data/furniture_dataset.csv
```

## API Endpoints

### POST /recommend
Get personalized recommendations

**Request:**
```json
{
  "query": "modern blue sofa",
  "top_k": 5,
  "filters": {
    "max_price": 1500,
    "material": "velvet"
  }
}
```

### GET /analytics
Get catalog analytics

### GET /products
List all products (paginated)

### GET /health
Health check

## Technology Stack

**Backend:** FastAPI, SentenceTransformers, scikit-learn, pandas, numpy  
**Frontend:** React, TailwindCSS, Recharts  
**DevOps:** Docker, Docker Compose

## Algorithm

Improved multi-factor scoring system for high-quality recommendations:

**Primary Factors:**
- 75% Text Semantic Similarity (SentenceTransformers with weighted embedding)
  - Title: 3x weight (most important)
  - Description: 2x weight  
  - Categories, Material, Color: 1x weight each
  
**Secondary Factors:**
- 15% Category Matching (expanded keyword list, weighted by field)
- 5% Material Matching (comprehensive material detection)
- 5% Color Matching (expanded color variations)

**Quality Controls:**
- Minimum similarity threshold: 0.45 (increased for better results)
- Automatic fallback if no keywords match (pure semantic similarity)
- Duplicate removal by product ID
- Post-filtering for price, category, material, color

## Configuration

**Backend (.env):**
```bash
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_PATH=data/furniture_dataset.csv
```

**Frontend (.env):**
```bash
REACT_APP_API_URL=http://localhost:8000
```

## License

MIT License

---

Built by FurniMatch AI Team

