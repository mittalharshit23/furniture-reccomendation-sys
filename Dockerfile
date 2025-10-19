# Multi-stage Dockerfile for Furniture Recommendation System
# Optimized for Render deployment - builds both frontend and backend

# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-build

WORKDIR /app

# Copy frontend package files
COPY frontend/package*.json .

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy frontend source
COPY frontend/ .

# Build the React app for production
RUN npm run build

# Stage 2: Backend with embedded Frontend
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ .

# Copy built frontend from previous stage to serve as static files
COPY --from=frontend-build /app/build /app/frontend_build

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Expose port (Render uses PORT env variable)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    API_HOST=0.0.0.0 \
    API_PORT=8000

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run the application (Render will use $PORT environment variable)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
