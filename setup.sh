#!/bin/bash

# Sales Training Voice Simulator - Setup & Run Script

echo "🎤 Sales Training Voice Simulator"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 16+"
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

echo "✓ Python 3 found"
echo "✓ Node.js found"
echo ""

# Setup Backend
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt
echo "✓ Backend dependencies installed"

# Setup Frontend
echo ""
echo "📦 Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    npm install --silent
fi

echo "✓ Frontend dependencies installed"

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo ""
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    python -m uvicorn app:app --reload"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd frontend"
echo "    npm run dev"
echo ""
echo "Then open: http://localhost:5173"
