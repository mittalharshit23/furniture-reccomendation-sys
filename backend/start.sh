#!/bin/bash

echo "🚀 Starting Furniture Recommendation System..."

# Start backend
echo "📦 Starting Backend..."
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend
sleep 5

# Start frontend
echo "🎨 Starting Frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

echo "✅ Both servers started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait