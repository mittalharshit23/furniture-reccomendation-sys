"""Configuration settings for the application."""
import os
from pathlib import Path

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/furniture_dataset.csv")

# CORS Configuration
CORS_ORIGINS = ["*"]

# Model Configuration
TEXT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Recommendation Settings
DEFAULT_TOP_K = 5
MIN_SIMILARITY_THRESHOLD = 0.45  # Increased from 0.3 for better quality
MAX_RESULTS = 10
SIMILARITY_WEIGHTS = {
    "text": 0.75,      # Increased from 0.7 - text similarity is most important
    "category": 0.15,
    "material": 0.05,  # Reduced from 0.08
    "color": 0.05      # Reduced from 0.07
}

